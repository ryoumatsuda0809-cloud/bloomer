import glob
import os
import sys
import time

import google.genai as genai
from supabase import create_client

sys.path.insert(0, os.path.dirname(__file__))
from chunk import parse_markdown


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"環境変数 {name} が設定されていません。ターミナルで export {name}=値 を実行してください。")
        sys.exit(1)
    return value


def main() -> None:
    supabase_url = _require_env("SUPABASE_URL")
    supabase_key = _require_env("SUPABASE_SERVICE_ROLE_KEY")
    gemini_api_key = _require_env("GEMINI_API_KEY")

    client = genai.Client(api_key=gemini_api_key)
    supabase = create_client(supabase_url, supabase_key)

    knowledge_dir = os.path.join(os.path.dirname(__file__), "..", "knowledge")
    md_files = [
        p for p in glob.glob(os.path.join(knowledge_dir, "*.md"))
        if os.path.basename(p) != ".gitkeep"
    ]

    success_count = 0
    error_count = 0

    for filepath in sorted(md_files):
        filename = os.path.basename(filepath)

        try:
            chunks = parse_markdown(filepath)
        except Exception as e:
            print(f"✗ {filename} - パースエラー: {e}")
            error_count += 1
            continue

        for idx, chunk in enumerate(chunks, start=1):
            start = time.time()
            search_text = f"{chunk['trigger']} / {chunk['fact']} / {chunk['insight']} / {chunk['quest_seed']}"

            try:
                result = client.models.embed_content(
                    model="models/gemini-embedding-2",
                    contents=search_text,
                    config={"output_dimensionality": 768},
                )
                embedding = result.embeddings[0].values

                supabase.table("knowledge_chunks").upsert(
                    {
                        "trigger": chunk["trigger"],
                        "fact": chunk["fact"],
                        "insight": chunk["insight"],
                        "quest_seed": chunk["quest_seed"],
                        "embedding": embedding,
                        "source": chunk["source_file"],
                    },
                    on_conflict="trigger",
                ).execute()

                elapsed = time.time() - start
                print(f"✓ {filename} - チャンク{idx}: {chunk['trigger']} ({elapsed:.1f}s)")
                success_count += 1

            except Exception as e:
                print(f"✗ {filename} - チャンク{idx}: {e}")
                error_count += 1

    print(f"\n完了: {success_count}件投入, {error_count}件スキップ（エラー）")


if __name__ == "__main__":
    main()
