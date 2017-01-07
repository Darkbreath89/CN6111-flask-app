from main import app
import unittest

class ErgasiaTestCase(unittest.TestCase):
	
	def setUp(self):
		# creates a test client
		self.app = app.test_client()
        # propagate the exceptions to the test client
		self.app.testing = True 

	def tearDown(self):
		pass
		
	#Tests
	def test_home_status_code(self):
		result=self.app.get('/')
		# assert the status code of the response
		self.assertEqual(result.status_code, 200) 
	def test_newpackage_status_code(self):	
		result=self.app.get('/NewPackage')
		# assert the status code of the response
		self.assertEqual(result.status_code, 200) 
	def test_packagesend_status_code(self):
		result=self.app.get('/PackageSend')
		# assert the status code of the response
		self.assertEqual(result.status_code, 200)
	def test_inventory_status_code(self):
		result=self.app.get('/Inventory')
		# assert the status code of the response
		self.assertEqual(result.status_code, 200)
	def test_code_post_NewPackage(self):
		result=self.app.post('/NewPackage')
		# assert the status code of the response
		self.assertEqual(result.status_code, 200)	
	def test_code_post_Inventory(self):
		for i in range(0-4):
			result=self.app.post('/PackageSend?radio='+i)
			# assert the status code of the response
			self.assertEqual(result.status_code, 200)		
	
		
if __name__=='__main__':
	unittest.main()

