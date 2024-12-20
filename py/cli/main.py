from cli.command_group import cli
from cli.commands import (
    collections,
    conversations,
    database,
    documents,
    graphs,
    indices,
    prompts,
    retrieval,
    system,
    users,
)
from cli.utils.telemetry import posthog, telemetry

# Chunks
cli.add_command(collections.collections)
cli.add_command(conversations.conversations)
cli.add_command(documents.documents)
cli.add_command(graphs.graphs)

# Graph
cli.add_command(indices.indices)
cli.add_command(prompts.prompts)
cli.add_command(retrieval.retrieval)
cli.add_command(users.users)
cli.add_command(system.system)

# Database
cli.add_command(database.db)
cli.add_command(database.upgrade)
cli.add_command(database.downgrade)
cli.add_command(database.current)
cli.add_command(database.history)

def main():
    try:
        cli()
    except SystemExit:
        # Silently exit without printing the traceback
        pass
    except Exception as e:
        # Handle other exceptions if needed
        print("CLI error: An error occurred")
        raise e
    finally:
        # Ensure all events are flushed before exiting
        if posthog:
            posthog.flush()
            posthog.shutdown()

if __name__ == "__main__":
    main()