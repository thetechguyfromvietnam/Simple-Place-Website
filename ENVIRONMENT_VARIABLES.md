# Environment Variables for Vercel Deployment

## Required Variables

Add these environment variables in your Vercel dashboard (Settings → Environment Variables):

### Email Configuration
```
EMAIL_USER=simpleplace199f@gmail.com
EMAIL_PASS=your-gmail-app-password-here
RESTAURANT_EMAIL=simpleplace199f@gmail.com
```

### Application Configuration
```
FRONTEND_URL=https://simpleplacevn.com
NODE_ENV=production
```

## How to Get Gmail App Password

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Click on "App passwords"
4. Select "Mail" as the app
5. Generate a new password
6. Use this password (not your regular Gmail password) for `EMAIL_PASS`

## Important Notes

- **Never use your regular Gmail password** - only use app passwords
- **Use your custom domain** `simpleplacevn.com` for FRONTEND_URL
- **Test locally first** before deploying to production
- **Monitor email usage** to avoid hitting Gmail limits

## Testing

After deployment, test these endpoints:
- `https://your-project-name.vercel.app/api/health`
- Submit a test order through the website
- Make a test booking through the website

Both should send confirmation emails to the restaurant and customer.
