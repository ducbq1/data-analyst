if (_listLns != null && _listLns.Count > 0)
{
  foreach (var model in _listLns)
  {
    model.PropertyChanged += (sender, args) =>
    {
      if (args.PropertyName == nameof(NsDanhMucCongKhaiCustomModel.IsChecked))
      {
        //TH1: Nếu check or uncheck cha thì check or uncheck all con
        var lstChild = ListLns.Where(x => x.iID_DMCongKhai_Cha == model.Id).ToList();
        var lstParent = ListLns.Where(x => x.Id == model.iID_DMCongKhai_Cha).ToList();
        var lstCheck = ListLns.Where(x => x.iID_DMCongKhai_Cha == model.iID_DMCongKhai_Cha).ToList();
        if (lstChild.Count() > 0 && lstChild.Any(x => x.IsChecked != model.IsChecked) && isActive)
        {
          lstChild.Select(x => { x.IsChecked = model.IsChecked; return x; }).ToList();
        }
        if (lstParent.Count() > 0)
        {
          isActive = false;
          if (!model.IsChecked || lstCheck.All(x => x.IsChecked)) //false
          {
            lstParent.Select(x => { x.IsChecked = model.IsChecked; return x; }).ToList();
          }
          isActive = true;
        }

        OnPropertyChanged(nameof(LabelSelectedCountLns));
        OnPropertyChanged(nameof(SelectAllLns));
      }
    };
  }
}



private string GetLevelTitle(DmChuKy dmChuKy, int level)
{
  var iLoaiDVBanHanh = dmChuKy.GetType().GetProperty("LoaiDVBanHanh" + level).GetValue(dmChuKy)?.ToString() ?? string.Empty;
  if (iLoaiDVBanHanh == LoaiDonViBanHanh.DON_VI_QUAN_LY)
  {
    return _danhMucService.FindByType(TypeDanhMuc.DM_CAUHINH, _sessionService.Current.YearOfWork).FirstOrDefault(n => n.IIDMaDanhMuc == MaDanhMuc.DV_QUANLY)?.SGiaTri ?? string.Empty;
  }
  else if (iLoaiDVBanHanh == LoaiDonViBanHanh.DON_VI_SU_DUNG)
  {
    return _sessionService.Current.TenDonVi;
  }
  else if (iLoaiDVBanHanh == LoaiDonViBanHanh.CAP_QUAN_LY_TAI_CHINH)
  {
    return _danhMucService.FindByType(TypeDanhMuc.DM_CAUHINH, _sessionService.Current.YearOfWork).FirstOrDefault(n => n.IIDMaDanhMuc == MaDanhMuc.DV_THONGTRI_BANHANH)?.SGiaTri ?? string.Empty;
  }
  else if (iLoaiDVBanHanh == LoaiDonViBanHanh.DON_VI_DUOC_CHON)
  {
    return "CÁC ĐƠN VỊ";
  }
  else if (iLoaiDVBanHanh == LoaiDonViBanHanh.TUY_CHINH)
  {
    return dmChuKy.GetType().GetProperty("TenDVBanHanh" + level).GetValue(dmChuKy)?.ToString() ?? string.Empty;
  }
  else
  {
    return string.Empty;
  }
}


public delegate void DataChangedEventHandler(object sender, EventArgs e);
public event DataChangedEventHandler ClosePopup;

private void OnCloseWindow()
{
  DataChangedEventHandler handler = ClosePopup;
  if (handler != null)
  {
    handler(this, new EventArgs());
  }
}

AllocationDetailViewModel.ClosePopup += RefreshAfterClosePopup;
private void RefreshAfterClosePopup(object sender, EventArgs e)
{
  try
  {
    view.Close();
    OnRefesh();
  }
  catch (Exception ex)
  {
    _logger.Error(ex.Message, ex);
  }
}