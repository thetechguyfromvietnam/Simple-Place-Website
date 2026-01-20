'use client'

export default function Visit() {
  return (
    <section id="visit" className="px-4 md:px-8 lg:px-12 pb-20">
      <div className="mx-auto max-w-6xl grid gap-8 md:grid-cols-2">
        {/* Hours Card */}
        <div className="rounded-2xl border bg-white hover:shadow-xl transition-shadow" data-aos="fade-up" data-aos-delay="200">
          <div className="p-6 border-b flex items-center gap-2">
            <span className="text-amber-600 text-lg">⏰</span>
            <h4 className="font-semibold text-lg">Hours</h4>
          </div>
          <div className="p-6 text-sm">
            <p className="text-neutral-600 mb-4">Walk-ins welcome • Reservations recommended on weekends</p>
            <div className="space-y-3">
              <div>
                <div className="font-medium text-base mb-1">Mỗi ngày / Every Day</div>
                <div className="text-neutral-700 text-lg font-semibold">10:00 – 22:00</div>
              </div>
              <div className="pt-3 border-t border-neutral-200">
                <div className="font-medium text-amber-700">⚠️ Lưu ý / Note:</div>
                <div className="text-neutral-600 mt-1">
                  Đóng cửa vào ngày Lễ Tết của Việt Nam (1 ngày)<br />
                  Closed on Vietnamese National Holidays (1 day)
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Location Card */}
        <div className="rounded-2xl border bg-white hover:shadow-lg transition-shadow" data-aos="fade-up" data-aos-delay="400">
          <div className="p-5 border-b">
            <h4 className="font-semibold">Location</h4>
            <p className="text-sm text-neutral-600">
              215B4 Nguyễn Văn Hưởng, phường An Khánh, Thủ Đức, Thành phố Hồ Chí Minh
            </p>
          </div>
          <div className="aspect-[16/10] w-full overflow-hidden rounded-xl shadow">
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3918.984844463624!2d106.72968057585686!3d10.812471389338468!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x317527df16b4efab%3A0x7e7862d6d7c4818b!2sSimple%20Place!5e0!3m2!1svi!2s!4v1768025098634!5m2!1svi!2s"
              width="100%"
              height="100%"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              title="Simple Place Location"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
