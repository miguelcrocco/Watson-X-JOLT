#!/usr/bin/env bash
set -x

orchestrate env activate wxo-main
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate knowledge-bases remove -n db2-knowledge
orchestrate agents remove -n ProductAssistant -k native
orchestrate agents remove -n db2_agent -k native