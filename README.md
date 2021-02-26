
Welcome to Sep-2020 CloudGuruChallenge
==============

[Event-Driven Python on AWS](https://acloudguru.com/blog/engineering/cloudguruchallenge-python-aws-etl) organized by [A Cloud Guru](https://acloudguru.com/).

Outcome
-------

[Visualization Dashboard](https://sep20cloudguruchallenge-spadeploywebsitebucket1e-1dqr7kpvnyk14.s3-us-west-2.amazonaws.com/index.html)

[Read my blog article about this project.]

|   | deployment status |
|----------|-------------------|
| Backend  | ![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZGZHNUNDS0JqSnNVSlhyU21zdDB1VnNETVlSVDl6NlV3R3FadHB3TkhYMm1aZlpJNTE5R1NqYUJsOGxrMWgxdkJzQ0w1Y09ibU5TRm5ZYnM4NXR3Mk93PSIsIml2UGFyYW1ldGVyU3BlYyI6IjFkaHQvNkJBR05WK1ZJZWkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)|
| Frontend | ![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiRjZFajBNNFlBcEpVall4VXgxTUY3SHFaR1hvcUtwd25lcjBqM21DQ0s2QU9RUityRDBNZXVjcnlpQ0N6SWl0dDdJSGRZRklmVXgwM1pKaDQ0a3M5NWtFPSIsIml2UGFyYW1ldGVyU3BlYyI6InF6aWtXVjJLc25HRklIY0UiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)|


Architecture Overview
-------
Data Pipeline (Backend) steps:
1. Job Scheduling : Implemented through Event Bridge rules.
2. Extraction: Implemented using Lambda function (python) to extract data directly from source github repository.
3. Transformation: Pandas module used to perform data processing tasks. Lambda function used to implement this step.
4. Load: Data has been loaded to DynamoDB as batch output. for daily incremental load, S3 bucket is used to refer previous run file.
5. Notification: SNS notification service has been implemented to notify the user after completion of the ETL job.

![Backend-DataPipeline - Cloudformation stack design](images/Backend-Stack-Design.png?raw=true "ETL")

![Backend-DataPipeline - AWS-Resources-Architecture Diagram](images/Backend-Resource-Architecture.png?raw=true "AWS-Resources")

Visualization (frontend) steps:
1. Another S3 bucket has been used to host frontend web-pages for this project.
2. An API Gateway service used to fetch data from Dynamodb, using lambda function. Please see below frontend architecture diagram.

![frontend-Visualization - Cloudformation stack design](images/Frontend-stack-Design.png?raw=true "ETL")

Helpful CDK Overview
-------
You should explore the contents of this project. It demonstrates a CDK app with two instances of a stack (`backend_stack`) and (`frontend_stack`).
which contains all AWS related resources as illustrated in below architecture diagram.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command. To learn more about CDK please go through official [AWS Documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html) .

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

References 
-------
[mostly from official CDK documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html)

Special Thanks: 
-------
[for Frontend Design](https://github.com/tbhagat/ETLChallengeBackEnd)

[for Bckend Design](https://github.com/dashmug/us-covid-stats)


Disclaimer: 
-------
- This project has been implemented just for learning purposes. Please implement all security features for production usage.
