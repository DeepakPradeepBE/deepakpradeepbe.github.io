data "aws_iam_policy_document" "scp_policy" {
  statement {
    sid    = "DenyAssignPublicIP"
    effect = "Deny"
    actions = [
      "ec2:CreateLaunchTemplate"
    ]
    resources = [
      "*"
    ]
    condition {
      test     = "BoolIfExists"
      variable = "ec2:AssociatePublicIpAddress"
      values = [
        "true"
      ]
    }
  }

  statement {
    sid    = "RestrictLaunchConfigCreation"
    effect = "Deny"
    actions = [
      "autoscaling:CreateLaunchConfiguration"
    ]
    resources = [
      "*"
    ]
  }
}
