# Simple Place Backend - Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Navigate to the server directory
```bash
cd server
```

### 4. Deploy to Vercel
```bash
vercel --prod
```

### 5. Set Environment Variables
After deployment, go to your Vercel dashboard and add these environment variables:

#### Required Environment Variables:
```
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-gmail-app-password
RESTAURANT_EMAIL=simpleplace@gmail.com
NODE_ENV=production
```

#### Optional Environment Variables:
```
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

## 📧 Email Setup (Important!)

### Gmail App Password Setup:
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → App passwords
3. Generate an app password for "Mail"
4. Use this app password (not your regular Gmail password) for `EMAIL_PASS`

### Alternative Email Services:
You can also use other email services by modifying the transporter configuration in `server.js`:
- **SendGrid**: More reliable for production
- **Mailgun**: Good alternative
- **Outlook/Hotmail**: Similar to Gmail setup

## 🔧 Configuration Details

### API Endpoints:
- **Health Check**: `GET /api/health`
- **Food Orders**: `POST /api/order`
- **Table Bookings**: `POST /api/book`

### CORS Configuration:
- Development: Allows `localhost:3000` and `localhost:5173`
- Production: Uses `FRONTEND_URL` environment variable or allows all origins

### Rate Limiting:
- Applied to `/api/book` endpoint
- 10 requests per 15 minutes per IP address

## 🌐 Frontend Integration

### Update Frontend API Base URL:
After deployment, update your frontend to use the Vercel backend URL:

```javascript
// Example for your frontend
const API_BASE_URL = 'https://your-backend-name.vercel.app/api';
```

### CORS Headers:
The backend is configured to accept requests from your frontend domain when `FRONTEND_URL` is set.

## 📊 Monitoring & Logs

### Vercel Dashboard:
- Monitor function invocations
- View logs and errors
- Check performance metrics

### Local Testing:
```bash
# Test locally
npm run dev

# Test endpoints
curl https://your-backend-name.vercel.app/api/health
```

## 🔒 Security Features

- **Helmet.js**: Security headers
- **CORS**: Cross-origin request protection
- **Rate Limiting**: Prevents spam
- **Input Validation**: Required field validation
- **Email Sanitization**: Basic email validation

## 🐛 Troubleshooting

### Common Issues:

1. **Email not sending**:
   - Check Gmail app password setup
   - Verify environment variables are set correctly
   - Check Vercel function logs

2. **CORS errors**:
   - Set `FRONTEND_URL` environment variable
   - Check frontend domain matches exactly

3. **Function timeouts**:
   - Vercel has a 10-second timeout for hobby plans
   - Consider upgrading for longer processing times

### Debug Mode:
Set `NODE_ENV=development` to enable detailed error logging.

## 📈 Scaling Considerations

### For Higher Traffic:
1. **Upgrade Vercel Plan**: For longer function execution times
2. **Database Integration**: Add MongoDB/PostgreSQL for data persistence
3. **Queue System**: Use Redis for handling high-volume emails
4. **Caching**: Implement Redis caching for frequently accessed data

### Database Options:
- **Vercel Postgres**: Easy integration with Vercel
- **MongoDB Atlas**: Popular NoSQL option
- **PlanetScale**: MySQL-compatible serverless database

## 🔄 Updates & Maintenance

### Redeploying:
```bash
vercel --prod
```

### Environment Variable Updates:
Update in Vercel dashboard → Settings → Environment Variables

### Code Updates:
1. Make changes to your code
2. Commit to git
3. Run `vercel --prod` or push to connected git branch

---

## 📞 Support

For issues with this deployment:
1. Check Vercel function logs
2. Verify environment variables
3. Test endpoints individually
4. Check email service configuration

**Restaurant Contact**: simpleplace@gmail.com | (+84) 904421089
