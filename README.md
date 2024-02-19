<!-- Simplified version of https://github.com/othneildrew/Best-README-Template -->

<!-- For "back to top" links -->
<a name="readme-top"></a>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a pair of simple python programs for backing up and restoring a directory to AWS S3.
This was completed as an assignment for my Cloud Computing course at the University of Washington Bothell,
and [`Specifications.pdf`](Specifications.pdf) is the specifications of the assignment.


### Built With

* [![Python][Python-shield]][Python-url]
* [![Amazon S3][AmazonS3-shield]][AmazonS3-url]
* [![Boto3][Boto3-shield]][Boto3-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Both programs are built in python and interact with AWS.
For either program to function, the following must be done first:

1. Create an [AWS](https://aws.amazon.com/) account.
2. [Download](https://aws.amazon.com/cli/) and configure the AWS CLI.
   ```commandline
   aws configure
   ```
3. [Download](https://www.python.org/downloads/) Python 3.9 or later.
   ```commandline
   python --version
   ```
4. Install Boto3.
   ```commandline
   pip install boto3
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage

To back up a directory, use the following command with your directory, bucket, and bucket directory:

```commandline
python -m src.backup.backup your_directory your_bucket::your_bucket_directory
```

or on some machines:

```commandline
python3 -m src.backup.backup your_directory your_bucket::your_bucket_directory
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Complete the backup program
- [ ] Complete the restore program
- [ ] Allow individual files to be backed up and restored

<p align="right">(<a href="#readme-top">back to top</a>)</p>



[Boto3-shield]:    https://img.shields.io/badge/Boto3-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white
[Boto3-url]:       https://aws.amazon.com/sdk-for-python/
[Python-shield]:   https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]:      https://www.python.org/
[AmazonS3-shield]: https://img.shields.io/badge/Amazon_S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white
[AmazonS3-url]:    https://aws.amazon.com/s3/
