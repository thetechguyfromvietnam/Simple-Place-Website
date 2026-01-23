import { NextRequest, NextResponse } from 'next/server'
import nodemailer from 'nodemailer'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { name, email, phone, date, time, guests, message } = body

    // Validate required fields
    if (!name || !email || !phone || !date || !time || !guests) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Format date and time
    const bookingDateTime = new Date(`${date}T${time}`)
    const formattedDateTime = bookingDateTime.toLocaleString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })

    const timestamp = new Date().toLocaleString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })

    // Send email notification
    const notificationEmail = process.env.NOTIFICATION_EMAIL
    const smtpHost = process.env.SMTP_HOST || 'smtp.gmail.com'
    const smtpPort = parseInt(process.env.SMTP_PORT || '587')
    const smtpUser = process.env.SMTP_USER
    const smtpPassword = process.env.SMTP_PASSWORD

    if (notificationEmail && smtpUser && smtpPassword) {
      try {
        // Create transporter
        const transporter = nodemailer.createTransport({
          host: smtpHost,
          port: smtpPort,
          secure: smtpPort === 465, // true for 465, false for other ports
          auth: {
            user: smtpUser,
            pass: smtpPassword,
          },
        })

        // Email content
        const emailSubject = `🔔 Đặt bàn mới - ${name}`
        const emailText = `
📅 ĐẶT BÀN MỚI

👤 Tên: ${name}
📧 Email: ${email}
📱 Số điện thoại: ${phone}
🕐 Ngày giờ: ${formattedDateTime}
👥 Số khách: ${guests}
💬 Ghi chú: ${message || 'Không có'}
⏰ Thời gian đặt: ${timestamp}

---
Simple Place - Booking System
        `.trim()

        const emailHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: #4285f4; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
    .content { background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }
    .info-row { margin: 15px 0; padding: 10px; background: white; border-radius: 4px; }
    .label { font-weight: bold; color: #666; }
    .footer { text-align: center; margin-top: 20px; color: #999; font-size: 12px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🔔 Đặt bàn mới</h1>
    </div>
    <div class="content">
      <div class="info-row">
        <span class="label">👤 Tên:</span> ${name}
      </div>
      <div class="info-row">
        <span class="label">📧 Email:</span> ${email}
      </div>
      <div class="info-row">
        <span class="label">📱 Số điện thoại:</span> ${phone}
      </div>
      <div class="info-row">
        <span class="label">🕐 Ngày giờ:</span> ${formattedDateTime}
      </div>
      <div class="info-row">
        <span class="label">👥 Số khách:</span> ${guests}
      </div>
      <div class="info-row">
        <span class="label">💬 Ghi chú:</span> ${message || 'Không có'}
      </div>
      <div class="info-row">
        <span class="label">⏰ Thời gian đặt:</span> ${timestamp}
      </div>
    </div>
    <div class="footer">
      Simple Place - Booking System
    </div>
  </div>
</body>
</html>
        `

        // Send email
        await transporter.sendMail({
          from: `"Simple Place" <${smtpUser}>`,
          to: notificationEmail,
          subject: emailSubject,
          text: emailText,
          html: emailHtml,
        })

        console.log('Email notification sent successfully')
      } catch (emailError: any) {
        console.error('Email notification error:', emailError)
        // Don't fail the request, booking was received
        return NextResponse.json({
          success: true,
          message: 'Booking received but failed to send email notification',
          warning: emailError.message,
        })
      }
    } else {
      // Log booking data if email is not configured
      console.log('Booking received (Email not configured):', {
        name,
        email,
        phone,
        date,
        time,
        guests,
        message
      })
    }

    return NextResponse.json({ 
      success: true,
      message: 'Booking request submitted successfully!' 
    })
  } catch (error: any) {
    console.error('Booking error:', error)
    return NextResponse.json(
      { error: 'Failed to submit booking', details: error.message },
      { status: 500 }
    )
  }
}
