#include "riderpage.h"
#include "ui_riderpage.h"

RiderPage::RiderPage(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::RiderPage)
{
    ui->setupUi(this);
}

RiderPage::~RiderPage()
{
    delete ui;
}
