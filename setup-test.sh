#!/bin/bash
current_dir=$(pwd)
deployment_dir="tests/vault/.obsidian/plugins/obsidian-protected-refs"

if [ ! -L ${deployment_dir} ]; then
    ln -s ${current_dir}/obsidian-plugin $deployment_dir
fi

