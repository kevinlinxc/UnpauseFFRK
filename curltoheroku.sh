#!/usr/bin/env bash
curl --netrc -X PATCH https://api.heroku.com/apps/unpauseffrk/formation \
  -d '{
  "updates": [
    {
      "type": "web",
      "docker_image": "sha256:b61f98ab9edecab4eeccf679f5b41e1965d755809d738b4b9cd39c10e6e25f2f"
    }
  ]
}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases"\
  -H "Authorization: Bearer 62916d7b-3780-4dc1-8eca-77408a9bafdf"

$SHELL