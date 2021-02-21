output "this_redshift_cluster_id" {
  description = "The availability zone of the RDS instance"
  value       = module.redshift.this_redshift_cluster_id
}

output "this_redshift_cluster_endpoint" {
  description = "Redshift endpoint"
  value       = module.redshift.this_redshift_cluster_endpoint
}

output "this_redshift_cluster_hostname" {
  description = "Redshift hostname"
  value       = module.redshift.this_redshift_cluster_hostname
}

output "redshift_iam_role_arn" {
    description = "IAM role for redshift"
    value       = aws_iam_role.redshift-iam-role.arn
}