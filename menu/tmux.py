import subprocess
from simple_term_menu import TerminalMenu


def list_tmux_sessions():
    tmux_command_output = subprocess.check_output(
        ["tmux", "list-sessions", "-F#{session_id}:#{session_name}"], universal_newlines=True
    )
    tmux_sessions = []
    for line in tmux_command_output.split("\n"):
        line = line.strip()
        if not line:
            continue
        session_id, session_name = tuple(line.split(":"))
        tmux_sessions.append((session_name, session_id))
    return tmux_sessions


def main():
    terminal_menu = TerminalMenu(
        ("|".join(session) for session in list_tmux_sessions()),
        preview_command="tmux capture-pane -e -p -t {}",
        preview_size=0.75,
    )
    menu_entry_index = terminal_menu.show()


if __name__ == "__main__":
    main()
