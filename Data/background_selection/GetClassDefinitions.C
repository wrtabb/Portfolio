
void GetClassDefinitions()
{
	TFile*file = new TFile("DYLL_M50toInf.root");
	TTree*tree = (TTree*)file->Get("recoTree/DYTree");
	tree->MakeClass();
}
