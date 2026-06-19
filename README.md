# 100hires-portfolio
# 100Hires Portfolio Project: Initial Setup

## Tools Installed
* **Cursor IDE** (Windows version)
* **Claude Code** (Cursor Extension)
* **Codex** (Cursor Extension)
* **Git** (Installed via Cursor's embedded AI)

## Steps Completed
1. Downloaded and installed Cursor IDE on my Windows PC.
2. Located and installed the Claude Code and Codex add-ons.
3. Created a new public repository on GitHub.
4. Linked my local Cursor environment to the remote GitHub repository.
5. Drafted, committed, and pushed this README.md file.

## Issues Encountered & Solutions

### 1. Locating Extensions in the New Cursor UI
* **The Issue:** The step-by-step instructions provided aligned with an older version of the Cursor interface. Finding the extensions in the latest Windows release proved difficult, and standard AI chatbots were unable to provide accurate UI navigation steps. 
* **The Solution:** I searched YouTube and found mostly outdated tutorials. After diving deeper into online forums and developer threads, I discovered a command-line workaround. By running `cursor --classic` in the Windows command prompt, I was able to launch the legacy interface, which allowed me to easily locate and install both extensions.

### 2. Claude Code Paywall
* **The Issue:** While signing into Codex was straightforward and free, Claude Code required a paid subscription to log in.
* **The Solution:** I researched free alternatives and found guides explaining how to use the Claude Code shell routed through different, free LLM models. To stay within the scope of the instructions without incurring costs, I installed the Claude Code extension as requested but opted not to complete the paid sign-in process.

### 3. Connecting Cursor AI to GitHub
* **The Issue:** After creating the GitHub repository, standard online tutorials for manually connecting the repository to Cursor were not working for my setup.
* **The Solution:** Rather than continuing to struggle with manual Git configurations, I decided to leverage the tools in front of me. I prompted Cursor AI's embedded assistant and shared the link to my GitHub repository. The AI successfully handled the Git installation and set up the connection, allowing me to commit and push this file seamlessly.

# B2B SaaS Cold Outreach Pipeline - Research

## Project Overview
This repository contains raw research, transcripts, and social content from 10 high-signal practitioners in the B2B SaaS outbound space. The goal is to synthesize this data into a modern, actionable cold outreach playbook.

## Source Selection Methodology
To ensure the resulting playbook is built on reality rather than theory, I explicitly filtered out high-level thought leaders. I prioritized **active practitioners**—founders building outbound engines, data-backed copywriters, and deliverability experts who actually practice what they preach.

See `/research/sources.md` for the complete annotated list and justification for each selection.

## Repository Structure
- `/research/sources.md` - Annotated list of 10 selected experts.
- `/research/youtube-transcripts/` - Raw video transcripts pulled via `youtube-transcript-api`.
- `/research/linkedin-posts/` - Collected LinkedIn content focusing on outbound tactics.
- `/research/other/` - Deliverability checklists and technical setup guides.