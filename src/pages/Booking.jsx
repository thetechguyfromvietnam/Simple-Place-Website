import { useState } from 'react'
import { motion } from 'framer-motion'
import { Calendar, Clock, Users, Phone, Mail, MessageSquare } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { format, addDays, startOfDay } from 'date-fns'
import { getApiUrl } from '../utils/api'

const Booking = () => {
  const [selectedDate, setSelectedDate] = useState('')
  const [selectedTime, setSelectedTime] = useState('')
  const [selectedGuests, setSelectedGuests] = useState(2)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [bookingId, setBookingId] = useState('')

  const { register, handleSubmit, formState: { errors }, reset } = useForm()

  const timeSlots = [
    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
    '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
    '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30'
  ]

  const guestOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

  // Generate available dates (next 30 days)
  const availableDates = Array.from({ length: 30 }, (_, i) => {
    const date = addDays(startOfDay(new Date()), i)
    return {
      value: format(date, 'yyyy-MM-dd'),
      label: format(date, 'MMM dd, yyyy'),
      day: format(date, 'EEEE')
    }
  })

  const onSubmit = async (data) => {
    setIsSubmitting(true)
    
    try {
      // Prepare booking data
      const bookingData = {
        ...data,
        date: selectedDate,
        time: selectedTime,
        guests: selectedGuests
      }
      
      console.log('Sending booking data:', bookingData)
      
      // Send booking to backend API
      const apiUrl = getApiUrl();
      console.log('API URL:', apiUrl);
      const response = await fetch(`${apiUrl}/api/book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingData)
      })
      
      const result = await response.json()
      
      if (result.success) {
        console.log('Booking successful:', result)
        setIsSubmitted(true)
        setBookingId(result.bookingId)
        reset()
        
        // Reset form after 8 seconds
        setTimeout(() => {
          setIsSubmitted(false)
          setSelectedDate('')
          setSelectedTime('')
          setSelectedGuests(2)
          setBookingId('')
        }, 8000)
      } else {
        throw new Error(result.message || 'Booking failed')
      }
      
    } catch (error) {
      console.error('Booking error:', error)
      alert(`Booking failed: ${error.message}. Please try again or call us at (+84) 904421089.`)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </motion.div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Booking Confirmed!</h2>
          <p className="text-gray-600 mb-4">
            ✅ Your reservation has been confirmed! Check your email for the confirmation details.
          </p>
          <div className="bg-green-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-green-800">
              📧 Confirmation email sent to your inbox
            </p>
            <p className="text-sm text-green-800">
              📧 Restaurant notification sent to our team
            </p>
          </div>
          <div className="bg-amber-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-amber-800">
              <strong>Booking ID:</strong> {bookingId}
            </p>
            <p className="text-sm text-amber-800">
              <strong>Contact:</strong> <a href="tel:+84904421089" className="text-amber-600 hover:underline">(+84) 904421089</a>
            </p>
          </div>
          <p className="text-sm text-gray-500">
            Please arrive 15 minutes before your reservation time. We look forward to serving you!
          </p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Book Your Table</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Reserve your spot at Simple Place for an unforgettable dining experience. 
            We recommend booking in advance, especially for weekends.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Booking Form */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* Date Selection */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
                    <Calendar size={20} className="text-amber-600" />
                    Select Date
                  </label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {availableDates.slice(0, 9).map((date) => (
                      <button
                        key={date.value}
                        type="button"
                        onClick={() => setSelectedDate(date.value)}
                        className={`p-3 rounded-xl border text-sm font-medium transition-all ${
                          selectedDate === date.value
                            ? 'border-amber-500 bg-amber-50 text-amber-700'
                            : 'border-gray-200 hover:border-amber-300 hover:bg-amber-50'
                        }`}
                      >
                        <div>{date.label}</div>
                        <div className="text-xs text-gray-500">{date.day}</div>
                      </button>
                    ))}
                  </div>
                  {errors.date && (
                    <p className="text-red-500 text-sm mt-1">Please select a date</p>
                  )}
                </div>

                {/* Time Selection */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
                    <Clock size={20} className="text-amber-600" />
                    Select Time
                  </label>
                  <div className="grid grid-cols-4 md:grid-cols-6 gap-3">
                    {timeSlots.map((time) => (
                      <button
                        key={time}
                        type="button"
                        onClick={() => setSelectedTime(time)}
                        className={`p-3 rounded-xl border text-sm font-medium transition-all ${
                          selectedTime === time
                            ? 'border-amber-500 bg-amber-50 text-amber-700'
                            : 'border-gray-200 hover:border-amber-300 hover:bg-amber-50'
                        }`}
                      >
                        {time}
                      </button>
                    ))}
                  </div>
                  {errors.time && (
                    <p className="text-red-500 text-sm mt-1">Please select a time</p>
                  )}
                </div>

                {/* Guests Selection */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
                    <Users size={20} className="text-amber-600" />
                    Number of Guests
                  </label>
                  <div className="grid grid-cols-5 md:grid-cols-6 gap-3">
                    {guestOptions.map((guests) => (
                      <button
                        key={guests}
                        type="button"
                        onClick={() => setSelectedGuests(guests)}
                        className={`p-3 rounded-xl border text-sm font-medium transition-all ${
                          selectedGuests === guests
                            ? 'border-amber-500 bg-amber-50 text-amber-700'
                            : 'border-gray-200 hover:border-amber-300 hover:bg-amber-50'
                        }`}
                      >
                        {guests}
                      </button>
                    ))}
                  </div>
                  <div className="mt-2 text-xs text-gray-500">
                    Need more than 20 guests? Please call us at (+84) 904421089
                  </div>
                </div>

                {/* Contact Information */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                      <Phone size={20} className="text-amber-600" />
                      Phone Number
                    </label>
                    <input
                      {...register('phone', { 
                        required: 'Phone number is required',
                        pattern: {
                          value: /^[0-9+\-\s()]+$/,
                          message: 'Please enter a valid phone number'
                        }
                      })}
                      type="tel"
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all"
                      placeholder="(+84) 123 456 789"
                    />
                    {errors.phone && (
                      <p className="text-red-500 text-sm mt-1">{errors.phone.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                      <Mail size={20} className="text-amber-600" />
                      Email
                    </label>
                    <input
                      {...register('email', { 
                        required: 'Email is required',
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: 'Please enter a valid email'
                        }
                      })}
                      type="email"
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all"
                      placeholder="your@email.com"
                    />
                    {errors.email && (
                      <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
                    )}
                  </div>
                </div>

                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <MessageSquare size={20} className="text-amber-600" />
                    Special Requests (Optional)
                  </label>
                  <textarea
                    {...register('specialRequests')}
                    rows={4}
                    className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all"
                    placeholder="Any dietary restrictions, allergies, or special occasions?"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting || !selectedDate || !selectedTime}
                  className="w-full bg-amber-500 text-white py-4 rounded-xl font-semibold hover:bg-amber-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center gap-2"
                >
                  {isSubmitting ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Processing...
                    </>
                  ) : (
                    'Confirm Reservation'
                  )}
                </button>
              </form>
            </div>
          </motion.div>

          {/* Booking Info Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            {/* Restaurant Info */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Restaurant Info</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Clock className="text-amber-600 mt-1" size={20} />
                  <div>
                    <p className="font-medium text-gray-900">Opening Hours</p>
                    <p className="text-sm text-gray-600">Everyday: 10:00-22:00</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Users className="text-amber-600 mt-1" size={20} />
                  <div>
                    <p className="font-medium text-gray-900">Capacity</p>
                    <p className="text-sm text-gray-600">No capacity limit - Large groups welcome</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Info */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Contact Us</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Phone className="text-amber-600" size={20} />
                  <a href="tel:+84904421089" className="text-gray-700 hover:text-amber-600 transition-colors">
                    (+84) 904421089
                  </a>
                </div>
                <div className="flex items-center gap-3">
                  <Mail className="text-amber-600" size={20} />
                  <a href="mailto:simpleplace@gmail.com" className="text-gray-700 hover:text-amber-600 transition-colors">
                    simpleplace@gmail.com
                  </a>
                </div>
              </div>
            </div>

            {/* Booking Policy */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Booking Policy</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Reservations are recommended for weekends</li>
                <li>• Please arrive within 15 minutes of your booking time</li>
                <li>• Cancellations should be made at least 2 hours in advance</li>
                <li>• Large groups welcome - no capacity limits</li>
                <li>• Open everyday from 10:00 AM to 10:00 PM</li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default Booking
