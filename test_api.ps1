# test_api.ps1
# 一键测试 Flask Workflow API
# 1. 发送 POST /workflows/from-prompt
# 2. 提取 workflow_id
# 3. GET /workflows/<id> 显示详情

# test_api.ps1  (ASCII-safe version)

$baseUrl = "http://127.0.0.1:5000/api"

# Use a here-string for the prompt; no quotes to escape.
$prompt = @'
Step 1: Applicant Info  Role: Applicant
Required input: Full Name
Required input: Date of Birth

Step 2: Officer Review  Role: Officer
Required input: Application ID
'@

# Build JSON body
$body = @{ prompt = $prompt } | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "POST /workflows/from-prompt ..."

# POST create
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/workflows/from-prompt" -Method Post -ContentType "application/json" -Body $body
} catch {
    Write-Host "POST failed: $($_.Exception.Message)"
    exit 1
}

Write-Host "Created workflow response:"
$response | ConvertTo-Json -Depth 10 | Write-Host

# Extract workflow_id
$workflow_id = $response.workflow_id
if (-not $workflow_id) {
    Write-Host "ERROR: workflow_id not found in response."
    exit 1
}

Write-Host ""
Write-Host "GET /workflows/$workflow_id ..."

# GET details
try {
    $workflow = Invoke-RestMethod -Uri "$baseUrl/workflows/$workflow_id" -Method Get -ContentType "application/json"
} catch {
    Write-Host "GET failed: $($_.Exception.Message)"
    exit 1
}

Write-Host "Workflow details:"
$workflow | ConvertTo-Json -Depth 10 | Write-Host

Write-Host ""
Write-Host "Done."
