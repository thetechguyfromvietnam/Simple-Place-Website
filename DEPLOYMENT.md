# Vercel Deployment Guide for Simple Place Website

## Overview
This guide will help you deploy your Simple Place restaurant website to Vercel with email functionality.

## Prerequisites
- Vercel account (free at vercel.com)
- Gmail account for email service
- Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Prepare Your Repository

### 1.1 Push to Git Repository
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Vercel deployment"

# Push to your remote repository
git remote add origin https://github.com/yourusername/simple-place-website.git
git push -u origin main
```

## Step 2: Set Up Gmail App Password

### 2.1 Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication if not already enabled

### 2.2 Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" as the app
3. Generate a new password
4. **Save this password** - you'll need it for Vercel environment variables

## Step 3: Deploy to Vercel

### 3.1 Connect Repository
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your Git repository
4. Vercel will automatically detect it's a React project

### 3.2 Configure Build Settings
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### 3.3 Set Environment Variables
In the Vercel dashboard, go to Settings → Environment Variables and add:

```
EMAIL_USER=simpleplace199f@gmail.com
EMAIL_PASS=your-gmail-app-password-here
RESTAURANT_EMAIL=simpleplace199f@gmail.com
FRONTEND_URL=https://simpleplacevn.com
NODE_ENV=production
```

**Important**: Replace `your-gmail-app-password-here` with the actual app password from Step 2.2

## Step 4: Deploy

### 4.1 Deploy Frontend
1. Click "Deploy" in Vercel
2. Wait for the build to complete
3. Your frontend will be available at `https://simpleplacevn.com` (after DNS setup)

### 4.2 Deploy Backend (API)
The backend is already configured to work with Vercel's serverless functions. The API endpoints will be available at:
- `https://simpleplacevn.com/api/health`
- `https://simpleplacevn.com/api/order`
- `https://simpleplacevn.com/api/book`

## Step 5: Test Email Functionality

### 5.1 Test Order Submission
1. Go to your deployed website
2. Add items to cart and place an order
3. Check that emails are sent to both restaurant and customer

### 5.2 Test Booking System
1. Go to the booking page
2. Make a reservation
3. Verify confirmation emails are sent

## Step 6: Custom Domain Setup (simpleplacevn.com)

### 6.1 Add Custom Domain to Vercel
1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain: `simpleplacevn.com`
3. Vercel will provide DNS configuration instructions

### 6.2 Configure DNS Records
You need to add these DNS records to your domain provider:

#### Option A: Apex Domain (simpleplacevn.com)
```
Type: A
Name: @
Value: 76.76.19.61
```

#### Option B: CNAME Record (if your provider supports it)
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

#### Option C: WWW Subdomain
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

### 6.3 Verify Domain
1. After adding DNS records, wait 5-10 minutes for propagation
2. In Vercel dashboard, click "Verify" next to your domain
3. Once verified, your site will be live at `https://simpleplacevn.com`

### 6.4 SSL Certificate
- Vercel automatically provides SSL certificates
- Your site will be accessible via HTTPS
- HTTP traffic will automatically redirect to HTTPS

## Troubleshooting

### Email Issues
- **Emails not sending**: Check that EMAIL_PASS is the app password, not your regular Gmail password
- **Authentication failed**: Ensure 2FA is enabled and app password is correct
- **Rate limiting**: Gmail has daily limits; consider upgrading to a paid email service for high volume

### Build Issues
- **Build fails**: Check that all dependencies are in package.json
- **API not working**: Verify environment variables are set correctly
- **CORS errors**: Ensure FRONTEND_URL matches your actual Vercel domain

### Performance
- **Slow API responses**: Vercel functions have a 10-second timeout on free plan
- **Cold starts**: First request after inactivity may be slower

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_USER` | Gmail address for sending emails | `simpleplace199f@gmail.com` |
| `EMAIL_PASS` | Gmail app password | `abcd efgh ijkl mnop` |
| `RESTAURANT_EMAIL` | Email to receive orders/bookings | `simpleplace199f@gmail.com` |
| `FRONTEND_URL` | Your custom domain URL | `https://simpleplacevn.com` |
| `NODE_ENV` | Environment mode | `production` |

## Security Notes

1. **Never commit environment variables** to your repository
2. **Use app passwords** instead of regular passwords
3. **Enable 2FA** on your Gmail account
4. **Monitor email usage** to avoid hitting Gmail limits
5. **Consider upgrading** to a dedicated email service for production use

## Support

If you encounter issues:
1. Check Vercel's function logs in the dashboard
2. Verify all environment variables are set
3. Test email configuration locally first
4. Check Gmail's security settings

## Next Steps

After successful deployment:
1. Set up monitoring and analytics
2. Configure custom domain
3. Set up automated backups
4. Consider upgrading to Vercel Pro for better performance
5. Implement database for order/booking persistence
