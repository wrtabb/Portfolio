#include "TMath.h"

int _nEvents = 10000;
float _mass = 39;

void Generate();
float GeneratePt(float xlow,float xhigh);
float GenerateEta(float xlow,float xhigh);
float GeneratePhi(float xlow,float xhigh);

vector<float> _leptonPt_lead;
vector<float> _leptonPt_sub;

void generate()
{
    Generate();
}// end generate();

void Generate()
{
    float dR,dEta,dPhi;
    float eta1,eta2;
    float phi1,phi2;
    float ptLead,ptSub;

    TH1F*hPtLead = new TH1F("hPtLead","",100,15,100);
    TH1F*hPtSub = new TH1F("hPtLead","",100,15,100);
    for(int i=0;i<_nEvents;i++){
        
        ptLead = GeneratePt(15,100);
        ptSub = GeneratePt(15,ptLead);

        hPtLead->Fill(ptLead);
        hPtSub->Fill(ptSub);
        _leptonPt_lead.push_back(ptLead);
        _leptonPt_sub.push_back(ptSub);
    }// end loop over events

    hPtLead->SetMarkerStyle(20);
    hPtLead->SetMarkerColor(kRed);
    hPtLead->SetLineColor(kRed);
    hPtSub->SetMarkerStyle(20);
    hPtSub->SetMarkerColor(kBlue);
    hPtSub->SetLineColor(kBlue);

    hPtSub->Draw("pe,same");
    hPtLead->Draw("pe,same");
}// end Generate()

float GeneratePt(float xmin,float xmax)
{
    TF1*ptFunc = new TF1("pt","[0]/(x+[1])",1,1000);
    ptFunc->SetParameter(0,1);
    ptFunc->SetParameter(2,1);

    float pt;
    pt = ptFunc->GetRandom(xmin,xmax);

    return pt;
}// end GeneratePt()

float GenerateEta(float xlow,float xhigh)
{
    float eta;
    return eta;
}// end GenerateEta()

float GeneratePhi(float xlow,float xhigh)
{
    float phi;
    return phi;
}// end GeneratePhi()
/*
float CalculateInvariantMass()
{
    TLorentzVector lepton1;
    TLorentzVector lepton2;

    lepton1.SetPtEtaPhiM(pt1,eta1,phi1,m1);
    lepton2.SetPtEtaPhiM(pt2,eta2,phi2,m2);

    float invMass = (lepton1+lepton2).M();
    return invMass;
}// end CalculateInvariantMass()
*/
