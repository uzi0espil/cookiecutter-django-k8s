#!/bin/bash

arrManifests=()

for FILE in ${GITHUB_WORKSPACE}/compose/kubernetes/configmaps/*.yaml; do
        arrManifests+=($FILE)
done

for FILE in ${GITHUB_WORKSPACE}/compose/kubernetes/secrets/*.yaml; do
        arrManifests+=($FILE)
done

for FILE in ${GITHUB_WORKSPACE}/compose/kubernetes/*.yaml; do
        arrManifests+=($FILE)
done

echo ${arrManifests[@]} | tr ' ' '\n'
