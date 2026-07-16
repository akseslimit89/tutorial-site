<?php
// Simple visitor counter - no database needed
$counterFile = __DIR__ . '/visitor_data.json';

// Initialize or read data
$data = ['total' => 0, 'today' => 0, 'yesterday' => 0, 'countries' => [], 'pages' => [], 'today_date' => ''];
if (file_exists($counterFile)) {
    $data = json_decode(file_get_contents($counterFile), true) ?? $data;
}

$today = date('Y-m-d');

// Reset today counter if new day
if ($data['today_date'] !== $today) {
    $data['yesterday'] = $data['today'];
    $data['today'] = 0;
    $data['today_date'] = $today;
}

// Count this visit
$data['total']++;
$data['today']++;

// Get country from IP (using free API)
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$country = 'Unknown';
if ($ip && $ip !== '127.0.0.1' && $ip !== '::1') {
    $countryData = @json_decode(file_get_contents("http://ip-api.com/json/{$ip}?fields=country,countryCode"), true);
    if ($countryData && isset($countryData['country'])) {
        $country = $countryData['country'] . ' (' . $countryData['countryCode'] . ')';
    }
}

// Count by country
if (!isset($data['countries'][$country])) $data['countries'][$country] = 0;
$data['countries'][$country]++;

// Count by page
$page = $_SERVER['HTTP_REFERER'] ?? 'direct';
$page = parse_url($page, PHP_URL_PATH) ?: '/';
if (!isset($data['pages'][$page])) $data['pages'][$page] = 0;
$data['pages'][$page]++;

// Save data
file_put_contents($counterFile, json_encode($data, JSON_PRETTY_PRINT));

// Return JSON
header('Content-Type: application/json');
echo json_encode([
    'total' => $data['total'],
    'today' => $data['today'],
    'country' => $country,
    'page' => $page
]);
