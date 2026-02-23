# ==============================================================================
# Script Name: openai_hybrid_board.py
# Description: This script simulates an AI Board of Directors. You can either 
#              pitch a new idea (which runs through local LM Studio officers 
#              first) OR load a previous markdown session to skip local inference 
#              and test the CEO directly. The CEO is powered by the OpenAI API 
#              and streams its executive summary in real-time. 
#
# Instructions for Use:
# 1. Install required library (if not already): pip install openai
# 2. Set your OpenAI API key as an environment variable:
#    - Mac/Linux: export OPENAI_API_KEY="your_api_key_here"
# 3. Open LM Studio, load your local model(s), and start the Local Server.
#    (Default port is 1234: http://localhost:1234/v1)
# 4. Run normally: python openai_hybrid_board.py
# 5. Run as a dry run (no API calls): python openai_hybrid_board.py --dry-run
# ==============================================================================

import argparse
import os
import sys
import datetime
import glob
from openai import OpenAI

# ------------------------------------------------------------------------------
# Configuration & System Prompts
# ------------------------------------------------------------------------------

# LM Studio Configuration
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lm-studio" 

# Define the local officers
OFFICERS = {
    "Technology Officer (CTO)": {
        "model": "local-model", 
        "system_prompt": (
            "You are the Chief Technology Officer. Analyze the provided idea focusing "
            "heavily on the technology stack. Break your analysis into two distinct sections: "
            "1. Hardware requirements and feasibility. 2. Software architecture and development. "
            "Be critical and concise."
        )
    },
    "Finance Officer (CFO)": {
        "model": "local-model",
        "system_prompt": (
            "You are the Chief Financial Officer. Analyze the provided idea focusing "
            "on financial viability, estimated costs, potential revenue streams, and funding "
            "requirements. Highlight any major financial risks."
        )
    },
    "Marketing Officer (CMO)": {
        "model": "local-model",
        "system_prompt": (
            "You are the Chief Marketing Officer. Analyze the provided idea focusing "
            "on the target audience, go-to-market strategy, branding, and competitive landscape. "
            "How do we sell this?"
        )
    },
    "General Opinion Officer": {
        "model": "local-model",
        "system_prompt": (
            "You are the General Opinion Officer. Analyze the provided idea focusing "
            "on overall public perception, ethical considerations, user experience, and "
            "practical real-world impact. Act as the voice of the common user."
        )
    }
}

# CEO Configuration
CEO_SYSTEM_PROMPT = (
    "You are the CEO. You will be provided with an original idea and the detailed "
    "evaluations from your Board of Directors (CTO, CFO, CMO, General Opinion). "
    "Synthesize their feedback into a cohesive, final executive summary. Make a final "
    "'Go/No-Go' decision and outline the immediate next steps."
)

# ------------------------------------------------------------------------------
# Core Logic
# ------------------------------------------------------------------------------

def get_local_officer_response(client, role_name, config, prompt, is_dry_run=False):
    """Handles the API call to the local LM Studio server."""
    print(f"[{role_name}] is analyzing the idea...")
    
    if is_dry_run:
        return f"[DRY RUN: Simulated {role_name} analysis report.]\n"
    
    try:
        response = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": config["system_prompt"]},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  -> [ERROR] Failed to get response from {role_name}: {e}")
        return f"[{role_name} failed to provide a report due to an error.]"

def stream_openai_ceo_response(client, prompt, is_dry_run=False):
    """Handles the streaming API call to OpenAI, prints it, and returns the full string."""
    print("\n[CEO] is reviewing the board's reports and synthesizing the final output...\n")
    print("==================================================")
    print("FINAL EXECUTIVE SUMMARY (CEO)")
    print("==================================================")
    
    if is_dry_run:
        dry_run_text = "[DRY RUN: Simulated CEO Executive Summary and Go/No-Go decision.]\n"
        print(dry_run_text)
        return dry_run_text
    
    full_response = ""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CEO_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                text_chunk = chunk.choices[0].delta.content
                print(text_chunk, end="", flush=True)
                full_response += text_chunk
        print("\n") 
        return full_response
        
    except Exception as e:
        error_msg = f"\n  -> [ERROR] Failed to stream response from CEO: {e}"
        print(error_msg)
        return full_response + error_msg

def export_to_markdown(idea, officer_reports, ceo_summary):
    """Saves the entire meeting context to a markdown file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"board_meeting_{timestamp}.md"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# AI Board of Directors Meeting\n\n")
            f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Original Idea\n")
            f.write(f"{idea}\n\n")
            f.write("---\n\n")
            
            f.write("## Officer Evaluations\n\n")
            for role, report in officer_reports.items():
                f.write(f"### {role}\n")
                f.write(f"{report}\n\n")
            f.write("---\n\n")
            
            f.write("## CEO Executive Summary\n\n")
            f.write(f"{ceo_summary}\n")
            
        print("==================================================")
        print(f"[SYSTEM] Full meeting successfully exported to: {filename}")
        print("==================================================")
    except Exception as e:
        print(f"\n[ERROR] Failed to save markdown file: {e}")

def load_previous_session():
    """Finds previous markdown sessions and lets the user select one to load."""
    files = sorted(glob.glob("board_meeting_*.md"), reverse=True)
    if not files:
        print("\n[SYSTEM] No previous session files found. Defaulting to new idea pitch.")
        return None, None
        
    print("\nFound previous sessions:")
    for i, f in enumerate(files):
        print(f"[{i+1}] {f}")
        
    try:
        sel = int(input("\nEnter the number of the session to load (or 0 to cancel and pitch new idea): "))
        if sel == 0 or sel > len(files) or sel < 1:
            print("[SYSTEM] Selection cancelled or invalid. Defaulting to new idea pitch.")
            return None, None
        
        filepath = files[sel-1]
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Strip out the old CEO summary so we only pass the Idea + Officer Reports
        if "## CEO Executive Summary" in content:
            context_for_ceo = content.split("## CEO Executive Summary")[0]
        else:
            context_for_ceo = content
            
        return filepath, context_for_ceo.strip()
    except ValueError:
        print("[SYSTEM] Invalid input. Defaulting to new idea pitch.")
        return None, None

def main():
    parser = argparse.ArgumentParser(description="Run the Hybrid AI Board of Directors with OpenAI CEO")
    parser.add_argument("--dry-run", action="store_true", help="Run the script without making API calls")
    args = parser.parse_args()

    # Setup API Keys
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key and not args.dry_run:
        print("ERROR: OPENAI_API_KEY environment variable not found.")
        print("Please set it before running the script (unless using --dry-run).")
        sys.exit(1)

    local_client = OpenAI(base_url=LM_STUDIO_BASE_URL, api_key=LM_STUDIO_API_KEY)
    
    if not args.dry_run:
        openai_client = OpenAI(api_key=openai_api_key)
    else:
        openai_client = None

    print("==================================================")
    print("AI BOARD OF DIRECTORS INITIALIZED")
    print("==================================================")
    
    if args.dry_run:
        print("*** DRY RUN MODE ACTIVE - NO API CALLS WILL BE MADE ***\n")

    is_loaded_session = False
    
    # Mode Selection
    try:
        print("Would you like to:")
        print("1. Pitch a new idea (Runs Local Officers + OpenAI CEO)")
        print("2. Evaluate a previous council session (Skips Local Officers, goes straight to OpenAI CEO)")
        choice = input("> ").strip()
    except KeyboardInterrupt:
        print("\nMeeting cancelled.")
        sys.exit(0)

    # --- PATH A: LOAD PREVIOUS SESSION ---
    if choice == '2':
        filepath, loaded_context = load_previous_session()
        if loaded_context:
            is_loaded_session = True
            print(f"\n[SYSTEM] Loaded context from {filepath}. Skipping local officers...")
            ceo_prompt = loaded_context

    # --- PATH B: NEW PITCH ---
    if not is_loaded_session:
        try:
            idea = input("\nPlease enter your idea to pitch to the Board: \n> ")
        except KeyboardInterrupt:
            print("\nMeeting cancelled.")
            sys.exit(0)
            
        if not idea.strip():
            print("No idea provided. Meeting adjourned.")
            sys.exit(0)

        print("\nStarting board evaluations...\n")

        officer_reports = {}
        for role, config in OFFICERS.items():
            report = get_local_officer_response(local_client, role, config, idea, is_dry_run=args.dry_run)
            officer_reports[role] = report

        ceo_prompt = f"ORIGINAL IDEA:\n{idea}\n\n"
        ceo_prompt += "BOARD EVALUATIONS:\n"
        for role, report in officer_reports.items():
            ceo_prompt += f"--- {role} ---\n{report}\n\n"

    # --- FINAL CEO SYNTHESIS (BOTH PATHS) ---
    ceo_summary = stream_openai_ceo_response(openai_client, ceo_prompt, is_dry_run=args.dry_run)

    # --- EXPORT HANDLING ---
    if is_loaded_session:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"board_meeting_revised_{timestamp}.md"
        try:
            with open(new_filename, "w", encoding="utf-8") as f:
                f.write(loaded_context + "\n\n## CEO Executive Summary (Revised)\n\n" + ceo_summary + "\n")
            print(f"[SYSTEM] Revised meeting exported to: {new_filename}")
        except Exception as e:
            print(f"\n[ERROR] Failed to save revised markdown file: {e}")
    else:
        export_to_markdown(idea, officer_reports, ceo_summary)

if __name__ == "__main__":
    main()