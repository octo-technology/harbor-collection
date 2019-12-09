ADMIN_USER=admin
ADMIN_PWD=Harbor12345
API_URL=http://localhost/api

function create_user {
  local user_name=$1

  local payload='{"username":"'"$user_name"'","email":"'"$user_name"'@example.com","realname":"'"$user_name"' user","password":"ChangeMe123","comment":null}'
   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX POST "$API_URL/users" -H 'content-type: application/json' -d "$payload"
  get_user_id "$user_name"
}

function get_user_by_name {
   curl -u "$ADMIN_USER:$ADMIN_PWD" -s "$API_URL/users?username=$1" | jq '.[0]'
}

function get_user_id {
  get_user_by_name "$1" | jq '.user_id'
}

function delete_user {
  local user_id=$1
   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX DELETE "$API_URL/users/$user_id"
}

function create_project {
  local project_name=$1

  local payload='{"project_name": "'"$project_name"'","metadata": {"public": "false"},"count_limit": -1,"storage_limit": 10737418240}'
   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX POST "$API_URL/projects" -H 'content-type: application/json' -d "$payload"
  get_project_id "$project_name"
}

function get_project_by_name {
   curl -u "$ADMIN_USER:$ADMIN_PWD" -s "$API_URL/projects?name=$1" | jq '.[0]'
}

function get_project_id {
  get_project_by_name "$1" | jq '.project_id'
}

function delete_project {
  local project_id=$1
   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX DELETE "$API_URL/projects/$project_id"
}

function get_project_members {
  local project_id=$1

   curl -u "$ADMIN_USER:$ADMIN_PWD" -s "$API_URL/projects/$project_id/members"
}

function add_admin_member_to_project {
  local user_name=$1
  local project_id=$2

  local payload='{"role_id":1,"member_user":{"username":"'"$user_name"'"}}'
   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX POST "$API_URL/projects/$project_id/members" -H 'content-type: application/json' -d "$payload"
}

function enable_autoscan_for_project {
  local project_id=$1

   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX PUT "$API_URL/projects/$project_id" -H 'content-type: application/json' -d '{"metadata":{"auto_scan":"true"}}'
}

function retain_versioned_images_in_project {
  local number_of_images_to_retain=$1
  local project_id=$2

  local payload=" { \"rules\": [{ \"disabled\": false, \"action\": \"retain\", \"params\": { \"latestPushedK\": ${number_of_images_to_retain} }, \"scope_selectors\": { \"repository\": [{ \"kind\": \"doublestar\", \"decoration\": \"repoMatches\", \"pattern\": \"**\" }] }, \"tag_selectors\": [{ \"kind\": \"doublestar\", \"decoration\": \"matches\", \"pattern\": \"*.*.*\" }], \"template\": \"latestPushedK\" }], \"algorithm\": \"or\", \"trigger\": { \"kind\": \"Schedule\", \"references\": {}, \"settings\": { \"cron\": \"\" } }, \"scope\": { \"level\": \"project\", \"ref\": ${project_id} } }"

   curl -u "$ADMIN_USER:$ADMIN_PWD" -sX POST "$API_URL/retentions" -H 'content-type: application/json' -d "$payload"
}


function provision_project {
  local project_name=$1

  local project_id=$(create_project "$project_name")
  local admin_name="${project_name}_admin"
  local admin_id=$(create_user "$admin_name")
  add_admin_member_to_project "$admin_name" "$project_id"
  enable_autoscan_for_project "$project_id"
  retain_versioned_images_in_project 5 "$project_id"
}

function destroy_project {
  local project_name=$1

  local project_id=$(get_project_id "$project_name")
  local admin_name="${project_name}_admin"
  local admin_id=$(get_user_id "$admin_name")
  delete_project "$project_id"
  delete_user "$admin_id"
}
