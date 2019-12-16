#!/bin/bash

GIT_REPO_BASE=$(git rev-parse --show-toplevel)
TARGETS_DIR="$GIT_REPO_BASE/tests/integration/targets"


cat <<EOF > cred_template.yml
---
harbor_url: "$HARBOR_URL"
harbor_admin_user: "$HARBOR_USERNAME"
harbor_admin_password: "$(echo -n $HARBOR_PASSWORD | base64 -d)"
EOF

for TARGET in $(ls $TARGETS_DIR); do
    [ ! -d "$TARGETS_DIR/$TARGET/vars" ] && mkdir $TARGETS_DIR/$TARGET/vars
    cp cred_template.yml $TARGETS_DIR/$TARGET/vars/main.yml
done
