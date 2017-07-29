<?php

//USAGE: php twitter.php
//looks for a post written at the hour that the cronjob is run, then posts it

require "vendor/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

include "./twitter_keys.php";
include "./twitter_posts.php";

date_default_timezone_set("America/New_York");

// TODO clean this up
function getConnectionWithAccessToken($consumer_token, $consumer_token_secret, $oauth_token, $oauth_token_secret) {
	$connection = new TwitterOAuth($consumer_token, $consumer_token_secret, $oauth_token, $oauth_token_secret);
	return $connection;
}
$connection = getConnectionWithAccessToken($consumer_key, $consumer_secret, $access_key, $access_secret);

$datestr = date("Y_m_d_H");
$varname = "post_".$datestr;
$file = 'twitter_log.txt';
if (isset($$varname)) {
	$status = $connection->post("statuses/update", ["status" => $$varname]);

	$datastr = $datestr."\n".json_encode($status)."\n\n";
	file_put_contents($file, $datastr, FILE_APPEND);
} else {
	file_put_contents($file, "nothing found for ".$datestr, FILE_APPEND);
}


?>