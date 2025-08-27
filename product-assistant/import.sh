#!/usr/bin/env bash
set -x

sh ./remove.sh

orchestrate env activate wxo-main
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

for knowledge_base in db2-knowledge.yaml; do
    orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_base/${knowledge_base}
done

for agent in db2-agent.yaml main-agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done