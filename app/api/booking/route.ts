import { NextRequest, NextResponse } from 'next/server'

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

    // Google Sheets API setup
    // Note: You'll need to install googleapis: npm install googleapis
    // And set up Google Service Account credentials in environment variables
    if (
      process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL &&
      process.env.GOOGLE_PRIVATE_KEY &&
      process.env.GOOGLE_SHEET_ID
    ) {
      try {
        const { google } = await import('googleapis')
        
        const auth = new google.auth.GoogleAuth({
          credentials: {
            client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
            private_key: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
          },
          scopes: ['https://www.googleapis.com/auth/spreadsheets'],
        })

        const sheets = google.sheets({ version: 'v4', auth })
        const spreadsheetId = process.env.GOOGLE_SHEET_ID

        // Append booking data to Google Sheet
        await sheets.spreadsheets.values.append({
          spreadsheetId,
          range: 'Bookings!A:G',
          valueInputOption: 'RAW',
          requestBody: {
            values: [[
              new Date().toISOString(),
              name,
              email,
              phone,
              `${date} ${time}`,
              guests,
              message || ''
            ]],
          },
        })
      } catch (sheetsError: any) {
        // Log error but don't fail the request
        console.error('Google Sheets error:', sheetsError)
        // In production, you might want to send to a logging service
      }
    } else {
      // Log booking data if Google Sheets is not configured
      console.log('Booking received (Google Sheets not configured):', {
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
