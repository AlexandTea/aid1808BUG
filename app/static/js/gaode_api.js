/**
 * Created by Python on 2018/12/17.
 */

function markLocation(mapId, address) {
    AMap.plugin('AMap.Geocoder', function() {
        var geocoder = new AMap.Geocoder();
        geocoder.getLocation(address, function(status, result) {
            if (status === 'complete' && result.info === 'OK') {
                // 经纬度
                var lng = result.geocodes[0].location.lng;
                var lat = result.geocodes[0].location.lat;

                // 地图实例
                var map = new AMap.Map(mapId, {
                    resizeEnable: true, // 允许缩放
                    center: [lng, lat], // 设置地图的中心点
                    zoom: 18, 　　　　　　 // 设置地图的缩放级别，0 - 20
                    });

                // 添加标记
                var marker = new AMap.Marker({
                    map: map,
                    position: new AMap.LngLat(lng, lat),   // 经纬度
                });
            } else {
                console.log('定位失败！');
                }
        });
    });
}
