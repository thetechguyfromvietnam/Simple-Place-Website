# Troubleshooting Blank Page Issues

## Common Causes and Solutions

### 1. **Vercel Configuration Issues**
- ✅ **Fixed**: Updated `vercel.json` with proper routing
- ✅ **Fixed**: Added explicit asset routing for CSS/JS files
- ✅ **Fixed**: Separated frontend and backend builds

### 2. **Build Configuration**
- ✅ **Fixed**: Added `base: '/'` to Vite config
- ✅ **Fixed**: Specified `assetsDir: 'assets'`

### 3. **Environment Variables**
Make sure these are set in Vercel dashboard:
```
EMAIL_USER=simpleplace199f@gmail.com
EMAIL_PASS=your-gmail-app-password
RESTAURANT_EMAIL=simpleplace199f@gmail.com
FRONTEND_URL=https://simpleplacevn.com
NODE_ENV=production
```

### 4. **Deployment Steps**
1. **Push changes to GitHub**
2. **Redeploy in Vercel** (or it will auto-deploy)
3. **Check Vercel function logs** for errors
4. **Test API endpoints**:
   - `https://your-domain.com/api/health`
   - `https://your-domain.com/api/order`
   - `https://your-domain.com/api/book`

### 5. **Debugging Steps**

#### Check Browser Console
- Open Developer Tools (F12)
- Look for JavaScript errors
- Check Network tab for failed requests

#### Check Vercel Logs
- Go to Vercel dashboard
- Click on your deployment
- Check "Functions" tab for errors

#### Test Locally First
```bash
npm run build
npm run preview
```
Visit `http://localhost:4173` to test the built version

### 6. **Common Issues**

#### Blank Page with No Errors
- Usually a routing issue
- Check that all assets are loading
- Verify `index.html` is being served

#### JavaScript Errors
- Check browser console
- Look for missing dependencies
- Verify environment variables

#### API Not Working
- Check environment variables
- Verify email configuration
- Test API endpoints directly

### 7. **Quick Fixes**

#### Force Redeploy
- In Vercel dashboard, click "Redeploy"
- Or push a small change to trigger redeploy

#### Clear Browser Cache
- Hard refresh (Ctrl+F5 or Cmd+Shift+R)
- Or open in incognito/private mode

#### Check Domain Configuration
- Verify DNS records are correct
- Wait for DNS propagation (up to 24 hours)

## Still Having Issues?

1. **Check Vercel deployment logs**
2. **Test the API health endpoint**
3. **Verify all environment variables are set**
4. **Try accessing the Vercel default domain first**

The updated configuration should resolve the blank page issue!
