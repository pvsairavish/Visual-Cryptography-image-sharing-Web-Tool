import os
import sys
import subprocess
import webbrowser

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "streamlit_app.py")

    print("=" * 60)
    print("  🔐 Starting Visual Cryptography Streamlit Web Tool...")
    print("=" * 60)
    print(f"Target script: {script_path}")
    print("Opening in your default browser at: http://localhost:8501")
    print("=" * 60)

    # Launch Streamlit using the current active Python interpreter
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        script_path,
        "--server.headless=false",
        "--browser.gatherUsageStats=false"
    ]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nStreamlit server stopped by user.")
    except Exception as e:
        print(f"Error launching Streamlit: {e}")
        # Direct fallback attempt
        try:
            from streamlit.web import bootstrap
            bootstrap.run(script_path, False, [], {})
        except Exception as inner_e:
            print(f"Direct bootstrap failed: {inner_e}")

if __name__ == "__main__":
    main()
