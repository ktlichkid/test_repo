import argparse
from .repo import TaskRepository
from .service import TaskService


def print_task(task) -> None:
    status = "[x]" if task.completed else "[ ]"
    print(f"{task.id} {status} {task.description}")


def cmd_add(args) -> int:
    svc = TaskService(TaskRepository())
    try:
        task = svc.add(args.description)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    print(f"Added task {task.id}: {task.description}")
    return 0


def cmd_list(args) -> int:
    svc = TaskService(TaskRepository())
    tasks = svc.list()
    if not tasks:
        print("No tasks yet.")
        return 0
    for t in tasks:
        print_task(t)
    return 0


def parse_task_id(s: str) -> int:
    try:
        val = int(s)
    except Exception:
        raise ValueError(f"Invalid id: {s}. Must be a positive integer")
    if val <= 0:
        raise ValueError(f"Invalid id: {s}. Must be a positive integer")
    return val


def cmd_complete(args) -> int:
    svc = TaskService(TaskRepository())
    try:
        task_id = parse_task_id(args.id)
        task = svc.complete(task_id)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    print(f"Completed task {task.id}: {task.description}")
    return 0


def cmd_delete(args) -> int:
    svc = TaskService(TaskRepository())
    try:
        task_id = parse_task_id(args.id)
        task = svc.delete(task_id)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    print(f"Deleted task {task.id}: {task.description}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="task", description="Personal Task Tracker v1")
    sub = p.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Task description")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.set_defaults(func=cmd_list)

    p_complete = sub.add_parser("complete", help="Mark a task as completed")
    p_complete.add_argument("id", help="Task id")
    p_complete.set_defaults(func=cmd_complete)

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", help="Task id")
    p_delete.set_defaults(func=cmd_delete)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
