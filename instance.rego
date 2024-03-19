package terraform

default allow = false

allow {
    input.resource_changes[_].type == "aws_instance"
    input.resource_changes[_].change.after.tags.Name == "OPA Instance"
}
