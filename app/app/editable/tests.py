from models import Placeholder, EditForm
import unittest


class TestAdminEdit(unittest.TestCase):
	"""Don't know if this is going to be of any help, but setUp() creates a Placeholder model and test_models() checks to see if it was, in fact, created. test_form() proves that you don't need the location field for an EditForm. You will need it however in the Django Admin site (But thats a different story). tearDown() then deletes the model in case you'd like to run the test over and over again.
Make sense??"""

	def setUp(self):
		location="test_block"
		content="<p>Do I exist?</p>"
		self.model = Placeholder.objects.create(location=location, content=content)
    	
	def test_models(self):
		self.assertEqual(self.model.location, "test_block")
		self.assertEqual(self.model.content, "<p>Do I exist?</p>")
    	
	def test_form(self):
		data = {'content':'<p>This is content.</p>'}
		self.form = EditForm(data)

		self.assertEqual(self.form.is_bound, True)
		self.assertEqual(self.form.is_valid(), True)
    
	def tearDown(self):
		self.model.delete()