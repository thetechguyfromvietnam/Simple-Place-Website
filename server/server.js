import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3002;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.NODE_ENV === 'production' ? process.env.FRONTEND_URL || '*' : ['http://localhost:3000', 'http://localhost:5173'],
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // limit each IP to 10 requests per windowMs
  message: 'Too many booking attempts, please try again later.'
});
app.use('/api/book', limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Email configuration
const createTransporter = () => {
  return nodemailer.createTransport({
    service: 'gmail', // You can change this to your email service
    auth: {
      user: process.env.EMAIL_USER || 'your-email@gmail.com',
      pass: process.env.EMAIL_PASS || 'your-app-password'
    }
  });
};

// Email templates
const createOrderEmailTemplate = (orderData) => {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>New Food Order - Simple Place</title>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f59e0b; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }
        .order-details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #f59e0b; }
        .item-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
        .item-name { font-weight: bold; }
        .item-price { color: #f59e0b; }
        .total-row { font-weight: bold; font-size: 1.1em; color: #f59e0b; }
        .detail-row { margin: 10px 0; }
        .label { font-weight: bold; color: #f59e0b; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>🍕 New Food Order - Simple Place</h1>
        </div>
        <div class="content">
          <p>A new food order has been placed at Simple Place restaurant.</p>
          
          <div class="order-details">
            <h3>Order Details</h3>
            <div class="detail-row">
              <span class="label">Order ID:</span> ${orderData.orderId}
            </div>
            <div class="detail-row">
              <span class="label">Customer Name:</span> ${orderData.fullName}
            </div>
            <div class="detail-row">
              <span class="label">Email:</span> ${orderData.email}
            </div>
            <div class="detail-row">
              <span class="label">Phone:</span> ${orderData.phone}
            </div>
            <div class="detail-row">
              <span class="label">Delivery Address:</span> ${orderData.address}
            </div>
            <div class="detail-row">
              <span class="label">Delivery Time:</span> ${orderData.deliveryTime}
            </div>
            <div class="detail-row">
              <span class="label">Special Instructions:</span> ${orderData.specialInstructions || 'None'}
            </div>
            <div class="detail-row">
              <span class="label">Order Time:</span> ${new Date(orderData.createdAt).toLocaleString('en-US')}
            </div>
          </div>
          
          <div class="order-details">
            <h3>Order Items (${orderData.totalItems} items)</h3>
            ${orderData.items.map(item => `
              <div class="item-row">
                <span class="item-name">${item.name} x${item.quantity}</span>
                <span class="item-price">${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(item.price * item.quantity)}</span>
              </div>
            `).join('')}
            <hr style="margin: 15px 0;">
            <div class="item-row total-row">
              <span>Total Amount:</span>
              <span>${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(orderData.totalPrice)}</span>
            </div>
          </div>
          
          <p><strong>Action Required:</strong> Please prepare this order and contact the customer when ready.</p>
          
          <div class="footer">
            <p>Simple Place Restaurant<br>
            199F Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh, Vietnam<br>
            Phone: (+84) 904421089 | Email: simpleplace@gmail.com<br>
            Open Everyday: 10:00 AM - 10:00 PM</p>
          </div>
        </div>
      </div>
    </body>
    </html>
  `;
};

const createOrderConfirmationEmailTemplate = (orderData) => {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Order Confirmation - Simple Place</title>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f59e0b; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }
        .order-details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #f59e0b; }
        .item-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
        .item-name { font-weight: bold; }
        .item-price { color: #f59e0b; }
        .total-row { font-weight: bold; font-size: 1.1em; color: #f59e0b; }
        .detail-row { margin: 10px 0; }
        .label { font-weight: bold; color: #f59e0b; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
        .highlight { background: #fff3cd; padding: 10px; border-radius: 5px; margin: 15px 0; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>✅ Order Confirmed - Simple Place</h1>
        </div>
        <div class="content">
          <p>Dear ${orderData.fullName},</p>
          
          <p>Thank you for your order! We're excited to prepare your delicious meal.</p>
          
          <div class="order-details">
            <h3>Your Order Details</h3>
            <div class="detail-row">
              <span class="label">Order ID:</span> ${orderData.orderId}
            </div>
            <div class="detail-row">
              <span class="label">Delivery Address:</span> ${orderData.address}
            </div>
            <div class="detail-row">
              <span class="label">Delivery Time:</span> ${orderData.deliveryTime}
            </div>
            <div class="detail-row">
              <span class="label">Special Instructions:</span> ${orderData.specialInstructions || 'None'}
            </div>
          </div>
          
          <div class="order-details">
            <h3>Order Items (${orderData.totalItems} items)</h3>
            ${orderData.items.map(item => `
              <div class="item-row">
                <span class="item-name">${item.name} x${item.quantity}</span>
                <span class="item-price">${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(item.price * item.quantity)}</span>
              </div>
            `).join('')}
            <hr style="margin: 15px 0;">
            <div class="item-row total-row">
              <span>Total Amount:</span>
              <span>${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(orderData.totalPrice)}</span>
            </div>
          </div>
          
          <div class="highlight">
            <strong>Important:</strong> We'll contact you when your order is ready for pickup/delivery. 
            If you need to make any changes, please call us at (+84) 904421089.
          </div>
          
          <p>We're excited to share our delicious Mexican-Vietnamese fusion cuisine with you!</p>
          
          <div class="footer">
            <p><strong>Simple Place Restaurant</strong><br>
            199F Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh, Vietnam<br>
            Phone: (+84) 904421089 | Email: simpleplace@gmail.com<br>
            Open Everyday: 10:00 AM - 10:00 PM</p>
          </div>
        </div>
      </div>
    </body>
    </html>
  `;
};

const createBookingEmailTemplate = (bookingData) => {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>New Booking - Simple Place</title>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f59e0b; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }
        .booking-details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #f59e0b; }
        .detail-row { margin: 10px 0; }
        .label { font-weight: bold; color: #f59e0b; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>🍕 New Booking - Simple Place</h1>
        </div>
        <div class="content">
          <p>A new booking has been made at Simple Place restaurant.</p>
          
          <div class="booking-details">
            <h3>Booking Details</h3>
            <div class="detail-row">
              <span class="label">Booking ID:</span> ${bookingData.bookingId}
            </div>
            <div class="detail-row">
              <span class="label">Customer Name:</span> ${bookingData.firstName} ${bookingData.lastName}
            </div>
            <div class="detail-row">
              <span class="label">Email:</span> ${bookingData.email}
            </div>
            <div class="detail-row">
              <span class="label">Phone:</span> ${bookingData.phone || 'Not provided'}
            </div>
            <div class="detail-row">
              <span class="label">Date:</span> ${new Date(bookingData.date).toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </div>
            <div class="detail-row">
              <span class="label">Time:</span> ${bookingData.time}
            </div>
            <div class="detail-row">
              <span class="label">Number of Guests:</span> ${bookingData.guests}
            </div>
            <div class="detail-row">
              <span class="label">Special Requests:</span> ${bookingData.specialRequests || 'None'}
            </div>
            <div class="detail-row">
              <span class="label">Booking Time:</span> ${new Date(bookingData.createdAt).toLocaleString('en-US')}
            </div>
          </div>
          
          <p><strong>Action Required:</strong> Please confirm this booking by calling the customer or responding to their email.</p>
          
          <div class="footer">
            <p>Simple Place Restaurant<br>
            199F Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh, Vietnam<br>
            Phone: (+84) 904421089 | Email: simpleplace@gmail.com<br>
            Open Everyday: 10:00 AM - 10:00 PM</p>
          </div>
        </div>
      </div>
    </body>
    </html>
  `;
};

const createConfirmationEmailTemplate = (bookingData) => {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Booking Confirmation - Simple Place</title>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f59e0b; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }
        .booking-details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #f59e0b; }
        .detail-row { margin: 10px 0; }
        .label { font-weight: bold; color: #f59e0b; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
        .highlight { background: #fff3cd; padding: 10px; border-radius: 5px; margin: 15px 0; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>✅ Booking Confirmed - Simple Place</h1>
        </div>
        <div class="content">
          <p>Dear ${bookingData.firstName},</p>
          
          <p>Thank you for choosing Simple Place! Your reservation has been received and we look forward to serving you.</p>
          
          <div class="booking-details">
            <h3>Your Booking Details</h3>
            <div class="detail-row">
              <span class="label">Booking ID:</span> ${bookingData.bookingId}
            </div>
            <div class="detail-row">
              <span class="label">Date:</span> ${new Date(bookingData.date).toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </div>
            <div class="detail-row">
              <span class="label">Time:</span> ${bookingData.time}
            </div>
            <div class="detail-row">
              <span class="label">Number of Guests:</span> ${bookingData.guests}
            </div>
            <div class="detail-row">
              <span class="label">Special Requests:</span> ${bookingData.specialRequests || 'None'}
            </div>
          </div>
          
          <div class="highlight">
            <strong>Important:</strong> Please arrive 15 minutes before your reservation time. 
            If you need to make any changes, please call us at (+84) 904421089.
          </div>
          
          <p>We're excited to share our delicious Mexican-Vietnamese fusion cuisine with you!</p>
          
          <div class="footer">
            <p><strong>Simple Place Restaurant</strong><br>
            199F Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh, Vietnam<br>
            Phone: (+84) 904421089 | Email: simpleplace@gmail.com<br>
            Open Everyday: 10:00 AM - 10:00 PM</p>
          </div>
        </div>
      </div>
    </body>
    </html>
  `;
};

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Simple Place API is running' });
});

app.post('/api/order', async (req, res) => {
  try {
    const orderData = req.body;
    
    // Validate required fields
    const requiredFields = ['fullName', 'email', 'phone', 'address', 'items', 'totalPrice'];
    const missingFields = requiredFields.filter(field => !orderData[field]);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Missing required fields: ${missingFields.join(', ')}`
      });
    }
    
    // Generate order ID and timestamp
    const orderId = `SP-${Date.now()}`;
    const createdAt = new Date().toISOString();
    
    const completeOrderData = {
      ...orderData,
      orderId,
      createdAt
    };
    
    // Create email transporter
    const transporter = createTransporter();
    
    // Send email to restaurant
    const restaurantEmailOptions = {
      from: process.env.EMAIL_USER || 'your-email@gmail.com',
      to: process.env.RESTAURANT_EMAIL || 'simpleplace@gmail.com',
      subject: `New Food Order - ${orderData.fullName} - ${orderData.totalItems} items`,
      html: createOrderEmailTemplate(completeOrderData)
    };
    
    // Send confirmation email to customer
    const customerEmailOptions = {
      from: process.env.EMAIL_USER || 'your-email@gmail.com',
      to: orderData.email,
      subject: `Order Confirmation - Simple Place - ${orderId}`,
      html: createOrderConfirmationEmailTemplate(completeOrderData)
    };
    
    // Send both emails
    await transporter.sendMail(restaurantEmailOptions);
    await transporter.sendMail(customerEmailOptions);
    
    // Log order (in production, save to database)
    console.log('New order received:', completeOrderData);
    
    res.json({
      success: true,
      message: 'Order confirmed successfully!',
      orderId,
      data: completeOrderData
    });
    
  } catch (error) {
    console.error('Order error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to process order. Please try again or call us directly.'
    });
  }
});

app.post('/api/book', async (req, res) => {
  try {
    const bookingData = req.body;
    
    // Validate required fields
    const requiredFields = ['firstName', 'lastName', 'email', 'date', 'time', 'guests'];
    const missingFields = requiredFields.filter(field => !bookingData[field]);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Missing required fields: ${missingFields.join(', ')}`
      });
    }
    
    // Validate booking date (not in the past)
    const bookingDate = new Date(bookingData.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (bookingDate < today) {
      return res.status(400).json({
        success: false,
        message: 'Cannot book for past dates'
      });
    }
    
    // Validate time slot (10:00-22:00)
    const time = bookingData.time;
    const timeRegex = /^([01]?[0-9]|2[0-1]):[0-5][0-9]$/;
    
    if (!timeRegex.test(time)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid time format'
      });
    }
    
    const [hours, minutes] = time.split(':').map(Number);
    const timeInMinutes = hours * 60 + minutes;
    const openingTime = 10 * 60; // 10:00 AM
    const closingTime = 22 * 60; // 10:00 PM
    
    if (timeInMinutes < openingTime || timeInMinutes >= closingTime) {
      return res.status(400).json({
        success: false,
        message: 'Booking time must be between 10:00 AM and 10:00 PM'
      });
    }
    
    // Validate guests (minimum 1, no maximum limit)
    if (bookingData.guests < 1) {
      return res.status(400).json({
        success: false,
        message: 'Minimum 1 guest required'
      });
    }
    
    // Generate booking ID and timestamp
    const bookingId = `SP${Date.now()}`;
    const createdAt = new Date().toISOString();
    
    const completeBookingData = {
      ...bookingData,
      bookingId,
      createdAt
    };
    
    // Create email transporter
    const transporter = createTransporter();
    
    // Send email to restaurant
    const restaurantEmailOptions = {
      from: process.env.EMAIL_USER || 'your-email@gmail.com',
      to: process.env.RESTAURANT_EMAIL || 'simpleplace@gmail.com',
      subject: `New Booking - ${bookingData.firstName} ${bookingData.lastName} - ${bookingData.date} at ${bookingData.time}`,
      html: createBookingEmailTemplate(completeBookingData)
    };
    
    // Send confirmation email to customer
    const customerEmailOptions = {
      from: process.env.EMAIL_USER || 'your-email@gmail.com',
      to: bookingData.email,
      subject: `Booking Confirmation - Simple Place - ${bookingData.date} at ${bookingData.time}`,
      html: createConfirmationEmailTemplate(completeBookingData)
    };
    
    // Send both emails
    await transporter.sendMail(restaurantEmailOptions);
    await transporter.sendMail(customerEmailOptions);
    
    // Log booking (in production, save to database)
    console.log('New booking received:', completeBookingData);
    
    res.json({
      success: true,
      message: 'Booking confirmed successfully!',
      bookingId,
      data: completeBookingData
    });
    
  } catch (error) {
    console.error('Booking error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to process booking. Please try again or call us directly.'
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'API endpoint not found'
  });
});

// For Vercel deployment
export default app;

// Only start server locally (not in Vercel)
if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => {
    console.log(`🚀 Simple Place API server running on port ${PORT}`);
    console.log(`📧 Email notifications enabled`);
    console.log(`🌐 CORS enabled for development`);
  });
}
