resource "aws_config_config_rule" "cw-custom-config-rule" {
  for_each = toset(var.cw-security-hub-id)
  name =  "${var.standards}-${each.key}-cw-custom-rule"

  source {
    owner             = "CUSTOM_LAMBDA"
    source_identifier = aws_lambda_function.aws-cw-custom-config-lambda.arn
  }

  input_parameters = jsonencode({
    "cloud_watch_control_id" = each.key,
    "cloudtrailLogGroup" = var.existing_all_region_trail_log_group == null ? aws_cloudtrail.cis_all_regions_trail[0].cloud_watch_logs_group_arn : var.existing_all_region_trail_log_group
  })

  depends_on = [
    aws_lambda_function.aws-cw-custom-config-lambda
  ]
}

resource "aws_config_remediation_configuration" "configrule-remediation" {
  for_each = toset(var.cw-security-hub-id)
  config_rule_name = aws_config_config_rule.cw-custom-config-rule[each.key].name
  target_type      = "SSM_DOCUMENT"
  target_id        = "AWS-PublishSNSNotification"
  target_version   = "1"

  parameter {
    name = "AutomationAssumeRole"
    static_value = aws_iam_role.cw-config-lambda-role.arn
  }
  parameter {
    name = "Message"
    static_value = each.key
  }
  parameter {
    name = "TopicArn"
    static_value = aws_sns_topic.aws-cw-config-remediation-topic.arn
  }

  automatic                  = true
  maximum_automatic_attempts = 10
  retry_attempt_seconds      = 600

  execution_controls {
    ssm_controls {
      concurrent_execution_rate_percentage = 25
      error_percentage                     = 20
    }
  }
}

