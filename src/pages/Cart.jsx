import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { useCart } from '../contexts/CartContext'
import { ShoppingCart, Plus, Minus, Trash2, CreditCard, MapPin, Clock, User, Mail, Phone } from 'lucide-react'
import { Link } from 'react-router-dom'

const Cart = () => {
  const { items, removeFromCart, updateQuantity, clearCart, getTotalPrice, getTotalItems } = useCart()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [orderId, setOrderId] = useState('')

  const { register, handleSubmit, formState: { errors }, reset } = useForm()

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price)
  }

  const onSubmit = async (data) => {
    setIsSubmitting(true)
    
    try {
      const orderData = {
        ...data,
        items: items,
        totalPrice: getTotalPrice(),
        totalItems: getTotalItems(),
        orderId: `SP-${Date.now()}`,
        createdAt: new Date().toISOString()
      }
      
      console.log('Sending order data:', orderData)
      
      // Send order to backend API
      const response = await fetch('http://localhost:3002/api/order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
      })
      
      const result = await response.json()
      
      if (result.success) {
        console.log('Order successful:', result)
        setIsSubmitted(true)
        setOrderId(result.orderId)
        clearCart()
        reset()
        
        // Reset form after 8 seconds
        setTimeout(() => {
          setIsSubmitted(false)
          setOrderId('')
        }, 8000)
      } else {
        throw new Error(result.message || 'Order failed')
      }
      
    } catch (error) {
      console.error('Order error:', error)
      alert(`Order failed: ${error.message}. Please try again or call us at (+84) 904421089.`)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
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
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Confirmed!</h2>
          <p className="text-gray-600 mb-4">
            ✅ Your food order has been confirmed! Check your email for the order details.
          </p>
          <div className="bg-green-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-green-800">
              📧 Order confirmation email sent to your inbox
            </p>
            <p className="text-sm text-green-800">
              📧 Restaurant notification sent to our team
            </p>
          </div>
          <div className="bg-amber-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-amber-800">
              <strong>Order ID:</strong> {orderId}
            </p>
            <p className="text-sm text-amber-800">
              <strong>Contact:</strong> <a href="tel:+84904421089" className="text-amber-600 hover:underline">(+84) 904421089</a>
            </p>
          </div>
          <p className="text-sm text-gray-500">
            We'll prepare your delicious meal and contact you when it's ready for pickup!
          </p>
        </motion.div>
      </div>
    )
  }

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-24 h-24 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-6"
          >
            <ShoppingCart size={40} className="text-amber-600" />
          </motion.div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Your Cart is Empty</h2>
          <p className="text-gray-600 mb-8 max-w-md">
            Looks like you haven't added any delicious items to your cart yet. Browse our menu and add some amazing dishes!
          </p>
          <Link
            to="/menu"
            className="btn-enhanced bg-amber-500 text-white px-8 py-3 rounded-xl font-semibold hover:bg-amber-600 transition-all duration-300 inline-flex items-center gap-2"
          >
            <ShoppingCart size={20} />
            Browse Menu
          </Link>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Cart</h1>
          <p className="text-gray-600">{getTotalItems()} items in your cart</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl shadow-lg p-4 sm:p-6"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Order Items</h2>
              <div className="space-y-4">
                {items.map((item, index) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:gap-4 p-3 sm:p-4 border border-gray-100 rounded-xl hover:shadow-md transition-shadow"
                  >
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-12 h-12 sm:w-16 sm:h-16 object-cover rounded-lg flex-shrink-0"
                    />
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 text-sm sm:text-base truncate">{item.name}</h3>
                      {item.size && (
                        <p className="text-xs text-amber-600 font-medium">
                          Size: {item.size}
                        </p>
                      )}
                      <p className="text-xs sm:text-sm text-gray-600">{formatPrice(item.price)} per {item.unit}</p>
                      <div className="flex items-center justify-between mt-2 sm:mt-0">
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                            className="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
                          >
                            <Minus size={12} className="sm:w-4 sm:h-4" />
                          </button>
                          <span className="w-6 sm:w-8 text-center font-semibold text-sm sm:text-base">{item.quantity}</span>
                          <button
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                            className="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
                          >
                            <Plus size={12} className="sm:w-4 sm:h-4" />
                          </button>
                        </div>
                        <div className="flex items-center gap-2">
                          <p className="font-semibold text-gray-900 text-sm sm:text-base">{formatPrice(item.price * item.quantity)}</p>
                          <button
                            onClick={() => removeFromCart(item.id)}
                            className="text-red-500 hover:text-red-700 transition-colors"
                          >
                            <Trash2 size={14} className="sm:w-4 sm:h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Order Form & Summary */}
          <div className="space-y-6">
            {/* Order Summary */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl shadow-lg p-4 sm:p-6"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Summary</h2>
              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <span>Items ({getTotalItems()})</span>
                  <span>{formatPrice(getTotalPrice())}</span>
                </div>
                <div className="flex justify-between">
                  <span>Delivery Fee</span>
                  <span className="text-green-600">Free</span>
                </div>
                <hr className="my-2" />
                <div className="flex justify-between font-bold text-lg">
                  <span>Total</span>
                  <span className="text-amber-600">{formatPrice(getTotalPrice())}</span>
                </div>
              </div>
              <button
                onClick={clearCart}
                className="w-full text-red-500 hover:text-red-700 font-medium py-2 transition-colors"
              >
                Clear Cart
              </button>
            </motion.div>

            {/* Customer Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl shadow-lg p-4 sm:p-6"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Delivery Information</h2>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <User size={16} className="inline mr-2" />
                    Full Name *
                  </label>
                  <input
                    {...register('fullName', { required: 'Full name is required' })}
                    type="text"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    placeholder="Enter your full name"
                  />
                  {errors.fullName && (
                    <p className="text-red-500 text-sm mt-1">{errors.fullName.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Phone size={16} className="inline mr-2" />
                    Phone Number *
                  </label>
                  <input
                    {...register('phone', { 
                      required: 'Phone number is required',
                      pattern: {
                        value: /^[+]?[0-9\s\-\(\)]{10,}$/,
                        message: 'Please enter a valid phone number'
                      }
                    })}
                    type="tel"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    placeholder="Enter your phone number"
                  />
                  {errors.phone && (
                    <p className="text-red-500 text-sm mt-1">{errors.phone.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Mail size={16} className="inline mr-2" />
                    Email Address *
                  </label>
                  <input
                    {...register('email', { 
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Please enter a valid email address'
                      }
                    })}
                    type="email"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    placeholder="Enter your email address"
                  />
                  {errors.email && (
                    <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <MapPin size={16} className="inline mr-2" />
                    Delivery Address *
                  </label>
                  <textarea
                    {...register('address', { required: 'Delivery address is required' })}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    placeholder="Enter your delivery address"
                  />
                  {errors.address && (
                    <p className="text-red-500 text-sm mt-1">{errors.address.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Clock size={16} className="inline mr-2" />
                    Delivery Time
                  </label>
                  <select
                    {...register('deliveryTime')}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  >
                    <option value="asap">ASAP (30-45 minutes)</option>
                    <option value="1hour">Within 1 hour</option>
                    <option value="2hours">Within 2 hours</option>
                    <option value="specific">Specific time (call to arrange)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Special Instructions
                  </label>
                  <textarea
                    {...register('specialInstructions')}
                    rows={2}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    placeholder="Any special instructions for your order?"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-amber-500 text-white py-4 rounded-xl font-semibold hover:bg-amber-600 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Processing Order...
                    </>
                  ) : (
                    <>
                      <CreditCard size={20} />
                      Place Order - {formatPrice(getTotalPrice())}
                    </>
                  )}
                </button>
              </form>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Cart
