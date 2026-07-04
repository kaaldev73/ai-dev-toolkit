import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

from commands import implement_command
from factories.work_item_factory import WorkItemFactory
from services.work_item_service import WorkItemService


def cmd_implement(args: list[str]) -> None:
    if not args:
        print("❌ Usage: cli.py implement <WORK-ITEM-ID> [prompt]")
        sys.exit(1)

    work_item_id = args[0]
    user_prompt = args[1] if len(args) > 1 else None

    try:
        output_path = implement_command.run(work_item_id, user_prompt)
        print(f"\n✅ Implementation response saved\n")
        print(f"ID      : {work_item_id}")
        print(f"Output  : {output_path}")
    except Exception as ex:
        print(f"\n❌ {ex}")
        sys.exit(1)


def cmd_create() -> None:
    print("\n===================================")
    print("      AI Engineering Toolkit")
    print("===================================\n")

    work_type = input(
        "Work Item Type (bug/feature/refactor): "
    ).strip().lower()

    title = input(
        "Title: "
    ).strip()

    try:

        work_item = WorkItemFactory.create(
            work_type=work_type,
            title=title,
        )

        folder = WorkItemService.create(
            work_item
        )

        print("\n✅ Work Item Created Successfully\n")

        print(f"ID      : {work_item.id}")
        print(f"Folder  : {folder}")

    except Exception as ex:
        print(f"\n❌ {ex}")
        sys.exit(1)


def main():
    args = sys.argv[1:]

    if args and args[0] == "implement":
        cmd_implement(args[1:])
    else:
        cmd_create()


if __name__ == "__main__":
    main()