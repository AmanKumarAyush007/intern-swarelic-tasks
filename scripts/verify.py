#!/usr/bin/env python3
import sys, io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
verify.py â€” Auto-grader for intern-swarelic-tasks

Usage:
    python verify.py --exercise 4.1 --user alice
    python verify.py --exercise 4.2 --user alice
    python verify.py --exercise 4.3 --user alice
    python verify.py --exercise 4.4 --user alice
    python verify.py --exercise 4.5 --user alice
    python verify.py --all-users --exercise 4.2
"""

import argparse
import ast
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# â”€â”€â”€ Colour helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(msg):   print(f"  {GREEN}âœ… {msg}{RESET}")
def fail(msg): print(f"  {RED}âŒ {msg}{RESET}")
def warn(msg): print(f"  {YELLOW}âš ï¸  {msg}{RESET}")


@dataclass
class Results:
    passed: int = 0
    failed: int = 0
    notes: list = field(default_factory=list)

    def record(self, success: bool, message: str, points: int = 1):
        if success:
            self.passed += points
            ok(message)
        else:
            self.failed += points
            fail(message)

    def summary(self, total_points: int):
        pct = (self.passed / total_points * 100) if total_points else 0
        print(f"\n{BOLD}{'â”€'*50}{RESET}")
        print(f"{BOLD}Score: {self.passed}/{total_points} ({pct:.0f}%){RESET}")
        if self.failed == 0:
            print(f"{GREEN}{BOLD}ðŸŽ‰ All checks passed!{RESET}")
        elif pct >= 70:
            print(f"{YELLOW}Almost there â€” fix the failing checks above.{RESET}")
        else:
            print(f"{RED}Needs significant work â€” review the exercise guide.{RESET}")


# â”€â”€â”€ Exercise 4.1 â€” Platform Exploration â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def check_41(submission_path: Path, r: Results):
    print(f"\n{BOLD}ðŸ“‹ Exercise 4.1 â€” Platform Exploration{RESET}")

    doc_file = submission_path / 'ARCHITECTURE_ANALYSIS.md'
    r.record(doc_file.exists(), "ARCHITECTURE_ANALYSIS.md exists", points=5)

    if doc_file.exists():
        content = doc_file.read_text(encoding='utf-8')
        word_count = len(content.split())
        r.record(word_count >= 800, f"Word count >= 800 (actual: {word_count})", points=10)

        required_sections = [
            ('Section 1', 'Codebase Map'),
            ('Section 2', 'Call Flow'),
            ('Section 3', 'Rules Engine'),
            ('Section 4', 'Multi-Tenant'),
            ('Section 5', 'Improvement'),
            ('Section 6', 'Question'),
        ]
        for section_id, keyword in required_sections:
            found = section_id in content or keyword in content
            r.record(found, f"  {section_id} ({keyword}) present", points=5)

        # Check for specificity in call flow section (must have file references)
        r.record('.py' in content, "References specific .py files in analysis", points=5)
        r.record('line' in content.lower() or 'L' in content,
                 "References specific line numbers", points=5)

        # Improvement opportunities
        r.record('Opportunity' in content or 'improvement' in content.lower(),
                 "Improvement opportunities section non-empty", points=5)

        # Check they didn't just copy the template
        r.record('_fill in_' not in content and 'Your answer' not in content,
                 "Document is filled in (not just the blank template)", points=10)


# â”€â”€â”€ Exercise 4.2 â€” Rules Engine â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def check_42(submission_path: Path, r: Results):
    print(f"\n{BOLD}ðŸ“‹ Exercise 4.2 â€” Rules Engine{RESET}")

    required_files = [
        'rules_engine/engine.py',
        'rules_engine/loader.py',
        'tests/test_engine.py',
    ]
    for f in required_files:
        r.record((submission_path / f).exists(), f"File exists: {f}", points=3)

    # Check engine.py implementation
    engine_file = submission_path / 'rules_engine/engine.py'
    if engine_file.exists():
        source = engine_file.read_text(encoding='utf-8')
        r.record('NotImplementedError' not in source or
                 source.count('NotImplementedError') == 0,
                 "All NotImplementedError stubs replaced with real code", points=10)
        r.record('evaluate' in source, "evaluate() method defined", points=5)
        r.record('matches' in source, "matches() method defined", points=5)

        # Check operator implementations
        for op in ['eq', 'gt', 'gte', 'lt', 'in', 'not_in', 'contains']:
            r.record(op in source, f"  Operator '{op}' handled", points=2)

        r.record('ValueError' in source, "ValueError raised for unknown operators", points=5)

    # Check loader.py
    loader_file = submission_path / 'rules_engine/loader.py'
    if loader_file.exists():
        source = loader_file.read_text(encoding='utf-8')
        r.record('json.load' in source, "JSON loading implemented", points=5)
        r.record('FileNotFoundError' in source, "FileNotFoundError raised for missing file", points=3)
        r.record('ValueError' in source, "ValueError raised for malformed rules", points=3)

    # Run the tests if pytest is available
    tests_dir = submission_path / 'tests'
    if tests_dir.exists():
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', str(tests_dir), '-v', '--tb=short', '-q'],
                capture_output=True, text=True, cwd=submission_path
            )
            test_passed = result.returncode == 0
            r.record(test_passed, f"pytest tests/ passes (exit code {result.returncode})", points=15)
            if not test_passed:
                print(f"    {YELLOW}{result.stdout[-500:] if len(result.stdout) > 500 else result.stdout}{RESET}")
        except Exception as e:
            warn(f"Could not run pytest: {e}")

    # Count test cases
    test_file = submission_path / 'tests/test_engine.py'
    if test_file.exists():
        source = test_file.read_text(encoding='utf-8')
        test_count = source.count('def test_')
        r.record(test_count >= 15, f"At least 15 test cases (found {test_count})", points=10)


# â”€â”€â”€ Exercise 4.3 â€” Agent Flow â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def check_43(submission_path: Path, r: Results):
    print(f"\n{BOLD}ðŸ“‹ Exercise 4.3 â€” Agent Flow State Machine{RESET}")

    required_files = [
        'agent_flow/state_machine.py',
        'agent_flow/session.py',
        'tests/test_state_machine.py',
    ]
    for f in required_files:
        r.record((submission_path / f).exists(), f"File exists: {f}", points=3)

    sm_file = submission_path / 'agent_flow/state_machine.py'
    if sm_file.exists():
        source = sm_file.read_text(encoding='utf-8')
        r.record('NotImplementedError' not in source or source.count('NotImplementedError') == 0,
                 "All NotImplementedError stubs replaced", points=10)

        # Check all states defined
        required_states = ['OFFLINE', 'ONLINE', 'AVAILABLE', 'RINGING', 'ON_CALL', 'WRAPPING_UP', 'BREAK']
        for state in required_states:
            r.record(state in source, f"  State {state} defined", points=2)

        # Check transitions list is non-empty
        r.record('StateTransition' in source and 'LOGIN' in source,
                 "TRANSITIONS list contains transitions (not empty)", points=10)

        r.record('InvalidTransitionError' in source, "InvalidTransitionError defined", points=5)
        r.record('history' in source, "history tracking implemented", points=5)

    session_file = submission_path / 'agent_flow/session.py'
    if session_file.exists():
        source = session_file.read_text(encoding='utf-8')
        r.record('get_metrics' in source, "get_metrics() method defined", points=5)
        r.record('calls_handled' in source, "calls_handled counter tracked", points=5)

    # Run tests
    tests_dir = submission_path / 'tests'
    if tests_dir.exists():
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', str(tests_dir), '-v', '--tb=short', '-q'],
                capture_output=True, text=True, cwd=submission_path
            )
            r.record(result.returncode == 0, f"pytest tests/ passes", points=15)
        except Exception as e:
            warn(f"Could not run pytest: {e}")

    test_file = submission_path / 'tests/test_state_machine.py'
    if test_file.exists():
        source = test_file.read_text(encoding='utf-8')
        test_count = source.count('def test_')
        r.record(test_count >= 12, f"At least 12 test cases (found {test_count})", points=10)


# â”€â”€â”€ Exercise 4.4 â€” API Client â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def check_44(submission_path: Path, r: Results):
    print(f"\n{BOLD}ðŸ“‹ Exercise 4.4 â€” SCAI API Client{RESET}")

    required_files = [
        'scai_client/__init__.py',
        'scai_client/config.py',
        'scai_client/auth.py',
        'scai_client/client.py',
        'scai_client/exceptions.py',
        'tests/test_client.py',
    ]
    for f in required_files:
        r.record((submission_path / f).exists(), f"File exists: {f}", points=2)

    # Check config
    config_file = submission_path / 'scai_client/config.py'
    if config_file.exists():
        source = config_file.read_text(encoding='utf-8')
        r.record('__post_init__' in source, "__post_init__ validation implemented", points=5)
        r.record('ValueError' in source, "ValueError raised on invalid config", points=5)

    # Check auth
    auth_file = submission_path / 'scai_client/auth.py'
    if auth_file.exists():
        source = auth_file.read_text(encoding='utf-8')
        r.record('NotImplementedError' not in source or source.count('NotImplementedError') == 0,
                 "All auth stubs implemented", points=10)
        r.record('expires_at' in source, "Token expiry tracked", points=5)
        r.record('REFRESH_THRESHOLD_SECS' in source or 'refresh' in source.lower(),
                 "Token refresh logic present", points=5)

    # Check client
    client_file = submission_path / 'scai_client/client.py'
    if client_file.exists():
        source = client_file.read_text(encoding='utf-8')
        r.record('NotImplementedError' not in source or source.count('NotImplementedError') == 0,
                 "All client stubs implemented", points=10)
        r.record('Authorization' in source, "Authorization header injected", points=5)
        r.record('raise_for_status' in source or 'status_code' in source,
                 "HTTP error handling present", points=5)
        r.record('SCAINotFoundError' in source, "SCAINotFoundError raised on 404", points=5)

    # Run tests
    tests_dir = submission_path / 'tests'
    if tests_dir.exists():
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', str(tests_dir), '-v', '--tb=short', '-q'],
                capture_output=True, text=True, cwd=submission_path
            )
            r.record(result.returncode == 0, "pytest tests/ passes", points=15)
        except Exception as e:
            warn(f"Could not run pytest: {e}")

    test_file = submission_path / 'tests/test_client.py'
    if test_file.exists():
        source = test_file.read_text(encoding='utf-8')
        test_count = source.count('def test_')
        r.record(test_count >= 10, f"At least 10 test cases (found {test_count})", points=10)


# â”€â”€â”€ Exercise 4.5 â€” Mini Feature â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def check_45(submission_path: Path, r: Results):
    print(f"\n{BOLD}ðŸ“‹ Exercise 4.5 â€” Mini Feature (Capstone){RESET}")

    r.record((submission_path / 'DESIGN_NOTES.md').exists(),
             "DESIGN_NOTES.md exists", points=10)
    r.record((submission_path / 'README.md').exists(),
             "README.md exists", points=5)
    r.record((submission_path / 'requirements.txt').exists(),
             "requirements.txt exists", points=5)

    design_notes = submission_path / 'DESIGN_NOTES.md'
    if design_notes.exists():
        content = design_notes.read_text(encoding='utf-8')
        word_count = len(content.split())
        r.record(word_count >= 300, f"DESIGN_NOTES word count >= 300 (actual: {word_count})", points=10)

        keywords = ['chose', 'decision', 'trade-off', 'edge case', 'would', 'time']
        found_keywords = sum(1 for kw in keywords if kw.lower() in content.lower())
        r.record(found_keywords >= 3, f"DESIGN_NOTES covers key reflection areas", points=10)

    # Check for models.py
    model_files = list(submission_path.rglob('models.py'))
    r.record(len(model_files) > 0, "models.py exists (data model defined)", points=10)

    if model_files:
        source = model_files[0].read_text(encoding='utf-8')
        r.record('models.Model' in source, "At least one Django model defined", points=10)

    # Check for serializers
    serializer_files = list(submission_path.rglob('serializers.py'))
    r.record(len(serializer_files) > 0, "serializers.py exists", points=5)

    # Check for tests
    test_files = list(submission_path.rglob('test_*.py'))
    r.record(len(test_files) > 0, "Test files present", points=10)
    if test_files:
        test_count = sum(
            f.read_text(encoding='utf-8').count('def test_') for f in test_files
        )
        r.record(test_count >= 10, f"At least 10 test cases (found {test_count})", points=15)

    # Check for views/API
    view_files = list(submission_path.rglob('views.py'))
    r.record(len(view_files) > 0, "views.py (API endpoints) present", points=10)


# â”€â”€â”€ Main â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
EXERCISE_MAP = {
    '4.1': (check_41, 65),
    '4.2': (check_42, 80),
    '4.3': (check_43, 80),
    '4.4': (check_44, 85),
    '4.5': (check_45, 100),
}


def find_submission(user: str, exercise: str) -> Path:
    repo_root = Path(__file__).parent.parent
    sub_path = repo_root / 'submissions' / user / exercise
    if sub_path.exists():
        return sub_path
    for ex_dir in (repo_root / 'exercises').iterdir():
        if ex_dir.name.startswith(exercise):
            return ex_dir
    raise FileNotFoundError(
        f"Submission not found for user='{user}', exercise='{exercise}'.\n"
        f"Expected at: {sub_path}"
    )


def main():
    parser = argparse.ArgumentParser(description='intern-swarelic-tasks verifier')
    parser.add_argument('--exercise', choices=list(EXERCISE_MAP.keys()))
    parser.add_argument('--user')
    parser.add_argument('--all-users', action='store_true')
    args = parser.parse_args()

    if not args.exercise:
        parser.error("--exercise is required")

    check_fn, total_points = EXERCISE_MAP[args.exercise]

    if args.all_users:
        repo_root = Path(__file__).parent.parent
        submissions_dir = repo_root / 'submissions'
        users = [d.name for d in submissions_dir.iterdir() if d.is_dir()] if submissions_dir.exists() else []
        if not users:
            print("No submissions found.")
            return
        for user in users:
            print(f"\n{'='*60}\n  {user}\n{'='*60}")
            try:
                path = find_submission(user, args.exercise)
                r = Results()
                check_fn(path, r)
                r.summary(total_points)
            except FileNotFoundError as e:
                warn(str(e))
    else:
        if not args.user:
            parser.error("--user is required")
        try:
            path = find_submission(args.user, args.exercise)
            r = Results()
            check_fn(path, r)
            r.summary(total_points)
        except FileNotFoundError as e:
            print(f"\033[91mError: {e}\033[0m")
            sys.exit(1)


if __name__ == '__main__':
    main()

