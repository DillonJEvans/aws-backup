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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Backup Screenshot][backup-screenshot]

This is a pair of simple command line programs for backing up and restoring a directory to AWS S3.
This was completed as an assignment for my Cloud Computing course at the University of Washington Bothell,
and [`Specifications.pdf`](Specifications.pdf) were the provided specifications of the assignment.


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

To back up a directory, use the following command:
```commandline
python -m src.backup.driver your_directory your_bucket::your_bucket_directory
```

To restore from a directory, use the following command:
```commandline
python -m src.restore.driver your_bucket::your_bucket_directory your_directory
```

Don't forget to replace your_directory, your_bucket, and your_bucket_directory
the appropriate command line arguments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [X] Complete the backup program.
  - [X] Add a progress bar and information.
  - [X] Polish the output at the start and end of the program.
- [X] Complete the restore program.
  - [X] Add a progress bar and information.
  - [X] Polish the output at the start and end of the program.
- [ ] Backup empty directories.
- [ ] Allow individual files to be backed up and restored.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Boto3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [README Template](https://github.com/othneildrew/Best-README-Template)
* [Img Shields](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



[backup-screenshot]:  images/backup_example.PNG
[restore-screenshot]: images/restore_example.PNG
[Boto3-shield]:       https://img.shields.io/badge/Boto3-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white
[Boto3-url]:          https://aws.amazon.com/sdk-for-python/
[Python-shield]:      https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]:         https://www.python.org/
[AmazonS3-shield]:    https://img.shields.io/badge/Amazon_S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white
[AmazonS3-url]:       https://aws.amazon.com/s3/
