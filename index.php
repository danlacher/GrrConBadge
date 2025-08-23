<?php
    $message = "";
    if ($_SERVER["REQUEST_METHOD"] === "POST") {
        $text = trim($_POST["user_input"]);
        if ($text !== "") {
            file_put_contents("submissions.txt", $text . PHP_EOL, FILE_APPEND | LOCK_EX);
            $message = "Saved!";
        }
    }
?>

<!DOCTYPE html>
<html>
    <head>
        <title>/dev/null GrrCon 2025 Badge Submission</title>
    </head>
    
    <body bgcolor="black">
	<center>
		<img width="304" height="384" src="https://grrcon.com/wp-content/uploads/2022/11/GrrCON_Skull2.png">
		<h1 style="color: green">Text to be displayed on<h1>
		<h1 style="color: green">/dev/null's badge</h1>
	        <form method="POST">
	            <input type="text" name="user_input" required>
	            <input type="submit" value="Submit">
	        </form>
	        <p>
	        <?php echo htmlspecialchars($message); ?></p>
    	</center>
	</font>
    </body>
</html>
