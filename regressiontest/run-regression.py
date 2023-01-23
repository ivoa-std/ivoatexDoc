#!/usr/bin/python3

import os
import subprocess
import tempfile
import traceback


def execute(cmd, check_output=None):
	"""execute a subprocess.Popen-compatible command cmd under supervision.

	Specifically, we run with shell=True so the ivoatexDoc recipes work as
	given in the spec.

	We bail out when either cmd's return code is non-0 or the assertion
	check_stdout is not met.  For now, that is: neither stdout nor stderr
	contains a string.
	"""
	output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
	output = output.decode("utf-8")
	if isinstance(check_output, str):
		assert check_output in output, f"'{check_output}' missing"
		print(output)


def do_edit(doc, to_replace, replacement):
	"""replaces to_replace with replacement in doc, making sure something 
	actually changed.
	"""
	changed = doc.replace(to_replace, replacement)
	assert doc!=changed, f"{to_replace} -> {replacement} didn't do anything"
	return changed


def edit_file(target_file, replacements):
	"""replaces target_file with a version with replacements applied.

	Each (old, new) replacement must change the document.
	"""
	with open(target_file, encoding="utf-8") as f:
		doc = f.read()

	for to_replace, replacement in replacements:
		doc = do_edit(doc, to_replace, replacement)
	
	with open(target_file, "w", encoding="utf-8") as f:
		f.write(doc)


def get_pdf_text(pdf_name):
	"""returns some sort of textual representation of the contents of pdf_name.
	"""
	return subprocess.check_output(["pdftotext", pdf_name, "-"]
		).decode("utf-8")


def edit_Makefile_template():
	#	Sect. 2.2.3, paragraph "Main metadata"
	edit_file("Makefile", [
		("DOCNAME = ????", "DOCNAME = Regress"),
		("DOCDATE = ???", "DOCDATE = 2023-02-01"),
		("DOCTYPE = ???", "DOCTYPE = NOTE")])


def edit_document_template():
	#	Sect. 2.2.3, paragraph "Additional metadata"
	edit_file("Regress.tex", [
			("???? Full title ????", "Regression test"),
			("???? group ????", "Standards and Processes"),
			("????URL????", "http://ivoa.net/authors/Fred/Test"),
			("????Alfred Usher Thor????", "Test, F."),
			("????Fred Offline????", "Other-Person, A. N."),
			("???? Abstract ????", "This is a document for a regression test.\n"
				"  It doesn't say anything interesting at all.  But it should\n"
				" press many buttons.\n\nLike multi-paragraph"
				" abstracts, for instance."),
			("???? Or remove the section header ????", "This regression test"
				" supported by the Martian Open Science Cloud project of the"
				" Mons Olympus philosophical society."),
			("??? Write something ????", "This is the start of nothing"),
			(r"\includegraphics[width=0.9\textwidth]{role_diagram.pdf}",
				"(no figure yet)"),
			("???? and so on, LaTeX as you know and love it. ????",
				"\section{Normative Nonsense}"),
		])


def test_basic_run():
	# Basically, make sure that a very basic LaTeX call works and yields a
	# plausible PDF.
	execute("make", "Output written on Regress.pdf (3 pages")

	built_text = get_pdf_text("Regress.pdf")
	assert "\nTest, F., Other-Person, A. N.\n" in built_text,\
		"Author processing broken"
	assert "This is an IVOA Note expressing" in built_text, "Status note?"
	assert "2 Normative Nonsense\n\n3" in built_text, "Missing ToC?"
	assert "‘Key words for use in RFCs to" in built_text,\
		"Bibliography missing?"


def run_tests():
		# Sect 2.2, opening
		os.environ["DOCNAME"] = "Regress"
		execute("mkdir $DOCNAME")
		os.chdir(os.environ["DOCNAME"])

		# Sect 2.2.2
		execute("git init")
		execute("git submodule add https://github.com/ivoa-std/ivoatex")
		execute("sh ivoatex/make-templates.sh $DOCNAME")
		execute('git commit -m "Starting $DOCNAME"')

		edit_Makefile_template()
		edit_document_template()

		test_basic_run()

def main():
	with tempfile.TemporaryDirectory("ivoatex") as dir:
		try:
			print(f"Testing in {dir}")
			os.chdir(dir)
			run_tests()
		except Exception as ex:
			traceback.print_exc()
			print(f"**Failure. Dumping you in a shell in the testbed.")
			print("Exit the shell to tear it down.")
			subprocess.call([os.environ.get("SHELL", "sh")])


if __name__=="__main__":
	main()
