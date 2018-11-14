#include "restpage.h"
#include "ui_restpage.h"

RestPage::RestPage(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::RestPage)
{
    ui->setupUi(this);
}

RestPage::~RestPage()
{
    delete ui;
}
