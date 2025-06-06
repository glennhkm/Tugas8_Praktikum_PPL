# Deployment Guide

This guide explains how to deploy the Electronic Store Management System to Vercel with AWS MySQL integration, including both manual deployment and CI/CD with GitHub.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Manual Deployment](#manual-deployment)
3. [CI/CD with GitHub](#cicd-with-github)
4. [Database Configuration](#database-configuration)
5. [Running Migrations](#running-migrations)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

1. A Vercel account
2. An existing AWS MySQL database
3. MySQL credentials (host, username, password, database name, port)
4. GitHub repository (for CI/CD)

## Manual Deployment

If you prefer to deploy manually, follow these steps:

### 1. Prepare Your Environment Variables

Make sure you have a `.env` file with the following variables:

```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your.aws.mysql.endpoint
DB_PORT=3306
DJANGO_INSECURE_SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 2. Run the Deployment Script

```bash
./deploy_complete.sh
```

This script:
- Installs required packages (PyMySQL, setuptools)
- Configures the simplified Vercel setup
- Creates a mock version of djangorestframework-simplejwt to avoid dependency issues
- Creates a .vercelignore file to exclude unnecessary files
- Deploys the application to Vercel

### 3. Configure Environment Variables in Vercel

After deployment, add all your environment variables in the Vercel dashboard.

## CI/CD with GitHub

For a more automated approach, you can set up continuous deployment with GitHub Actions.

### 1. Connect GitHub to Vercel

1. Go to the Vercel dashboard
2. Click "Add New Project"
3. Select your GitHub repository
4. Configure the project settings
5. Click "Deploy"

### 2. Get Vercel Credentials

You need three pieces of information from Vercel:

#### Vercel API Token

1. Go to your [Vercel account settings](https://vercel.com/account/tokens)
2. Click "Create" to create a new token
3. Give it a name like "GitHub Actions"
4. Copy the token value

#### Vercel Organization and Project IDs

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Link your project:
   ```bash
   vercel link
   ```

3. Check the `.vercel/project.json` file:
   ```bash
   cat .vercel/project.json
   ```

   You'll see something like:
   ```json
   {
     "orgId": "your-org-id",
     "projectId": "your-project-id"
   }
   ```

### 3. Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add the following secrets:
   - `VERCEL_TOKEN`: Your Vercel API token
   - `VERCEL_ORG_ID`: Your Vercel organization ID
   - `VERCEL_PROJECT_ID`: Your Vercel project ID

### 4. Verify Workflow Files

Ensure these files exist in your repository:

1. `.github/workflows/vercel-deploy.yml` - For production deployments
2. `.github/workflows/vercel-preview.yml` - For preview deployments

### 5. How CI/CD Works

- When you push to the `main` branch, GitHub Actions will automatically deploy to production
- When you create a pull request, a preview deployment will be created

## Database Configuration

### Configure AWS MySQL for Vercel Access

Ensure your AWS MySQL security group allows connections from Vercel's IP ranges:

1. Find Vercel's IP ranges in their documentation
2. Add these IP ranges to your AWS MySQL security group's inbound rules
3. Alternatively, you can temporarily allow connections from anywhere (0.0.0.0/0) for testing

## Running Migrations

For a fresh deployment, you may need to run migrations manually:

```bash
python manage.py migrate
```

## Troubleshooting

### Database Connection Issues

1. Verify your environment variables in the Vercel dashboard
2. Check if your AWS MySQL instance allows connections from Vercel's IP addresses
3. Ensure your database user has proper permissions

### Static Files Issues

If static files aren't loading:
1. Consider using a service like AWS S3 or Cloudinary for static files
2. Update your settings.py to use these services

### CI/CD Issues

1. Check GitHub Actions logs for errors in the "Actions" tab
2. Verify that all required secrets are set in GitHub
3. Ensure your Vercel token has the necessary permissions

## Important Notes

1. **Security**: Make sure your MySQL credentials are secure
2. **Performance**: AWS MySQL might have higher latency when accessed from Vercel
3. **Costs**: Be aware of potential costs for both Vercel and AWS MySQL 