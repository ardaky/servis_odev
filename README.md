# RectangleArea Servisi (ROS 2 Humble)

Dikdörtgenin genişlik ve yüksekliğini alıp alanını döndüren bir ROS 2 servisi.

| Paket | İçerik |
|---|---|
| `alan_interfaces` | `srv/RectangleArea.srv`: istek `width`, `height`; yanıt `area` (hepsi `float64`) ve `success` (`bool`) |
| `alan_py` | `alan_server`: servisi sunar, `area = width × height` döndürür<br>`alan_client`: komut satırından iki sayı alıp servisi çağırır |

**Bonus:** Yanıtta `bool success` alanı var. `width` veya `height` negatifse sunucu isteği reddeder (`success: False`, `area: 0.0`).

## Servis tanımı

```
float64 width
float64 height
---
float64 area
bool success
```

## Kurulum

```bash
# Paketleri bir workspace'in src klasörüne koyun
cp -r alan_interfaces alan_py ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select alan_interfaces alan_py
source install/setup.bash
```

## Çalıştırma

**Terminal 1 (sunucu):**

```bash
ros2 run alan_py alan_server
```

**Terminal 2 (istemci):**

```bash
ros2 run alan_py alan_client 3 4
ros2 run alan_py alan_client 2.5 -1
```

## Doğrulama: `ros2 service call`

```bash
ros2 service call /rectangle_area alan_interfaces/srv/RectangleArea "{width: 5.0, height: 2.5}"
ros2 service call /rectangle_area alan_interfaces/srv/RectangleArea "{width: -3.0, height: 4.0}"
```

## Çıktılar

### Arayüz

```
$ ros2 interface show alan_interfaces/srv/RectangleArea
float64 width
float64 height
---
float64 area
bool success
```

### İstemci

```
$ ros2 run alan_py alan_client 3 4
[INFO] [rectangle_area_client]: Alan: 3.0 x 4.0 = 12.0

$ ros2 run alan_py alan_client 2.5 -1
[ERROR] [rectangle_area_client]: Sunucu istegi reddetti (negatif deger): 2.5, -1.0
```

### `ros2 service call`

```
$ ros2 service call /rectangle_area alan_interfaces/srv/RectangleArea "{width: 5.0, height: 2.5}"
requester: making request: alan_interfaces.srv.RectangleArea_Request(width=5.0, height=2.5)

response:
alan_interfaces.srv.RectangleArea_Response(area=12.5, success=True)

$ ros2 service call /rectangle_area alan_interfaces/srv/RectangleArea "{width: -3.0, height: 4.0}"
requester: making request: alan_interfaces.srv.RectangleArea_Request(width=-3.0, height=4.0)

response:
alan_interfaces.srv.RectangleArea_Response(area=0.0, success=False)
```

### Sunucu logu

```
[INFO] [rectangle_area_server]: RectangleArea servisi hazir.
[INFO] [rectangle_area_server]: 3.0 x 4.0 = 12.0
[WARN] [rectangle_area_server]: Reddedildi: negatif deger (width=2.5, height=-1.0)
[INFO] [rectangle_area_server]: 5.0 x 2.5 = 12.5
[WARN] [rectangle_area_server]: Reddedildi: negatif deger (width=-3.0, height=4.0)
```

## Ekran görüntüsü

![Terminal ekran görüntüsü](ekran_goruntusu.png)
