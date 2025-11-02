# Simple Place Booking API

This is the backend API server for the Simple Place restaurant booking system with email notifications.

## Features

- ✅ Restaurant booking endpoint
- 📧 Email notifications to restaurant and customer
- 🔒 Rate limiting and security
- 🛡️ CORS protection
- 📱 Mobile-friendly booking system

## Setup Instructions

### 1. Install Dependencies

```bash
cd server
npm install
```

### 2. Email Configuration

1. **Create a Gmail App Password:**
   - Go to your Google Account settings
   - Enable 2-factor authentication
   - Generate an App Password for "Mail"
   - Copy the 16-character password

2. **Create Environment File:**
   ```bash
   cp env.example .env
   ```

3. **Update .env with your email details:**
   ```env
   EMAIL_USER=simpleplace199f@gmail.com
   EMAIL_PASS=your-16-character-app-password
   RESTAURANT_EMAIL=simpleplace199f@gmail.com
   PORT=3002
   NODE_ENV=development
   ```

### 3. Start the Server

```bash
# Development mode (with auto-restart)
npm run dev

# Production mode
npm start
```

The server will start on `http://localhost:3002`

## API Endpoints

### POST /api/book
Creates a new booking and sends email notifications.

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+84901234567",
  "date": "2024-01-15",
  "time": "19:00",
  "guests": 4,
  "specialRequests": "Birthday celebration"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Booking confirmed successfully!",
  "bookingId": "SP1704067200000",
  "data": { ... }
}
```

### GET /api/health
Health check endpoint.

## Email Templates

The system sends two emails:

1. **Restaurant Notification** - Sent to `RESTAURANT_EMAIL`
   - Contains all booking details
   - Includes customer contact information
   - Formatted for easy reading

2. **Customer Confirmation** - Sent to customer's email
   - Booking confirmation with details
   - Restaurant contact information
   - Arrival instructions

## Security Features

- **Rate Limiting**: 10 requests per 15 minutes per IP
- **Helmet.js**: Security headers
- **CORS**: Cross-origin resource sharing protection
- **Input Validation**: Required field validation
- **Error Handling**: Comprehensive error management

## Production Deployment

1. **Update CORS origin** in `server.js`:
   ```javascript
   origin: 'https://yourdomain.com'
   ```

2. **Set environment variables:**
   ```env
   NODE_ENV=production
   PORT=3001
   ```

3. **Deploy to your hosting service** (Heroku, DigitalOcean, AWS, etc.)

## Troubleshooting

### Email Not Working?
- Check your Gmail App Password is correct
- Ensure 2-factor authentication is enabled
- Verify the email addresses in your .env file

### CORS Errors?
- Update the CORS origin in server.js
- Make sure your frontend URL is correct

### Port Already in Use?
- Change the PORT in your .env file
- Kill any existing processes on that port

## Support

For issues or questions, contact:
- Phone: (+84) 904421089
- Email: simpleplace@gmail.com
