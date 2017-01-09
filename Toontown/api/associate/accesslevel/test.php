<?php
$hash = hash('sha256', openssl_random_pseudo_bytes(32));
echo $hash;

?>