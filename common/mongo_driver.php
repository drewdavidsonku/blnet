<?php
require '../vendor/autoload.php';
require "db_info_load.php";
class DB {
	private $db;

	public function __construct($config_arr) {
		$this->connect($config_arr);
	}
	
	private function connect($config_arr) {
		$connection = new MongoDB\Client($config_arr["db_connection_str"]);
		if ($connection->connected) {
			$this->db = $connection->blnet;
			return true;	
		} else {
			error_log("Could not connect to db");
			return false;
		}
	}

	public function getAllBooks() {
		$all_books = [];
		$cursor = $this->db->titleToISBN->find(); 
		foreach ($cursor as $document) {
			$all_books[$document['_id']] = $document['author'];
		}
		return $all_books;
	}

	public function getBookMetaData($title) {
		$cursor = $this->db->titleToISBN->find(["_id" => $title], ['limit' => 1]);
		$cursor->setTypeMap(['root' => 'array', 'document' => 'array', 'array' => 'array']);
		$allIsbns = current($cursor->toArray())["ISBN"];


		$options = array('limit'=>count($allIsbns), 'sort'=>array('date'=>-1));
		$cursor = $this->db->isbnData->find(array("_id" => array('$in'=>$allIsbns)), $options);
		$cursor->setTypeMap(['root' => 'array', 'document' => 'array', 'array' => 'array']);
		$allMetaData = [];
		foreach($cursor as $indData) {
			$allMetaData[] = $indData;	
		}
		# if (count($allIsbns) == 1)
		# 	return array($allMetaData);
		return $allMetaData;
	}

	public function getGeneralBookData($bookTitle) {
		$cursor = $this->db->titleToISBN->find(["_id" => $bookTitle], ['limit'=>1]);
		$cursor->setTypeMap(['root' => 'array', 'document' => 'array', 'array' => 'array']);
		return current($cursor->toArray());

	}

	public function getBooksTimeInterval($start, $end) {
		$cursor = $this->db->isbnData->find(array('date'=>array('$gte'=>$start, '$lte'=>$end)));
		$cursor->setTypeMap(['root' => 'array', 'document' => 'array', 'array' => 'array']);
		$isbn_results = [];
		foreach($cursor as $data) {
			$isbn_results[] = $data["_id"];
		}

		$cursor = $this->db->titleToISBN->find(array('ISBN'=>array('$in'=>$isbn_results)));
		$cursor->setTypeMap(['root' => 'array', 'document' => 'array', 'array' => 'array']);
		$results = [];
		foreach($cursor as $data) {
			$results[] = $data;
		}

		return $results;
	}
}

$global_db = new DB($config);
?>
