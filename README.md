# CFn template for SageMaker Studio Code Editor

This sample CloudFormation template creates an [Amazon SageMaker Studio Code Editor](https://docs.aws.amazon.com/sagemaker/latest/dg/code-editor.html), which provides a cloud-based IDE based on [Code-OSS, Visual Studio Code - Open Source](https://github.com/microsoft/vscode#visual-studio-code---open-source-code---oss). It has the [AWS Toolkit for VS Code extension](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html) pre-installed, which enables connections to AWS services such as [Amazon Q Developer](https://aws.amazon.com/q/developer/).

This template includes an additional feature that automatically stops Code Editor after a certain period of inactivity.

## Parameters

- `AutoStopIdleTimeInMinutes` : Idle time before auto-stop of Code Editor (disabled if 0)
- `EbsSizeInGb` : EBS volume size of Code Editor
- `InstanceType` : Instance type of Code Editor

## Deployment (1-click)

To deploy the Code Editor within your default VPC, click the "Launch Stack" button for the corresponding region. The deployment will take approximately 5-10 minutes.

|   AWS Region   |                                                                                                                                                                                   CloudFormation 1-Click URL                                                                                                                                                                                   |
| :------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|   us-east-1    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|   us-east-2    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-cmh-8d6e9c21a4dec77d.s3.us-east-2.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|   us-west-1    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://us-west-1.console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-sfo-f61fc67057535f1b.s3.us-west-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|   us-west-2    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-pdx-f3b3f9f1a7d6a3d0.s3.us-west-2.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
| ap-northeast-1 | [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ap-northeast-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-nrt-2cb4b4649d0e0f94.s3.ap-northeast-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml) |
| ap-northeast-2 | [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ap-northeast-2.console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-icn-ced060f0d38bc0b0.s3.ap-northeast-2.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml) |
| ap-northeast-3 | [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ap-northeast-3.console.aws.amazon.com/cloudformation/home?region=ap-northeast-3#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-kix-c2a28ad4e55ea53a.s3.ap-northeast-3.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml) |
| ap-southeast-1 | [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ap-southeast-1.console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-sin-694a125e41645312.s3.ap-southeast-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml) |
| ap-southeast-2 | [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ap-southeast-2.console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-syd-b04c62a5f16f7b2e.s3.ap-southeast-2.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml) |
|   ap-south-1   |       [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-bom-431207042d319a2d.s3.ap-south-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)       |
|   eu-north-1   |       [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://eu-north-1.console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-arn-580aeca3990cef5a.s3.eu-north-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)       |
|  eu-central-1  |    [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-fra-b129423e91500967.s3.eu-central-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)    |
|   eu-west-1    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-dub-85e3be25bd827406.s3.eu-west-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|   eu-west-2    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://eu-west-2.console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-lhr-cc4472a651221311.s3.eu-west-2.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|   eu-west-3    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://eu-west-3.console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-cdg-9e76383c31ad6229.s3.eu-west-3.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|   sa-east-1    |        [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://sa-east-1.console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-gru-527b8c19222c1182.s3.sa-east-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)         |
|  ca-central-1  |    [![Cloudformation Launch Stack button](images/cloudformation-launch-stack.png)](https://ca-central-1.console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=CodeEditorStack&templateURL=https://ws-assets-prod-iad-r-yul-5c2977cd61bca1f3.s3.ca-central-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/cloudformation/CodeEditorStack.template.yaml)    |

## Deployment (CLI)

```bash
aws cloudformation deploy \
    --template-file CodeEditorStack.template.yaml \
    --stack-name CodeEditorStack \
    --capabilities CAPABILITY_NAMED_IAM
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
