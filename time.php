<?php
header('Content-Type: application/json; charset=utf-8');
date_default_timezone_set('Asia/Ho_Chi_Minh');

// Lấy thời gian hiện tại của server
$now = new DateTime();

// Trả về theo định dạng ISO 8601
echo json_encode([
    'datetime' => $now->format('Y-m-d\TH:i:sP')
]);
