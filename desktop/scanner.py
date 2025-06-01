import cv2

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("📷 Arahkan QR code ke kamera... (tekan 'q' untuk batal)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"✅ QR Code terbaca: {data}")
            cap.release()
            cv2.destroyAllWindows()
            return data
        else:
            cv2.imshow("Scan QR Pasien", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
