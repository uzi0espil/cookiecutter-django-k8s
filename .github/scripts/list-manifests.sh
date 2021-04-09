#!/bin/bash

arrManifests=()

for FILE in compose/kubernetes/configmaps/*.yaml; do
        arrManifests+=($FILE)
done

for FILE in compose/kubernetes/secrets/*.yaml; do
        arrManifests+=($FILE)
done

for FILE in compose/kubernetes/*.yaml; do
        arrManifests+=($FILE)
done

echo ${arrManifests[@]} | tr ' ' '\n'
